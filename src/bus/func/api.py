# -*- coding: utf-8 -*-
from functools import wraps
from sanic import response
from src.bus.log.config import logger
import sys, os
import json
from src.bus.common.util import StrictJSONEncoder


def api_call(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        # just wrapper the request param
        response_code = 200
        result = 'mod success'
        try:
            result = await func(request, *args, **kwargs)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(exc_type, fname, exc_tb.tb_lineno)
            result = str(e)
            response_code = 400

        res = dict(result=result, status=response_code)
        res = json.loads(json.dumps(res, cls=StrictJSONEncoder))
        return response.json(res, status=response_code)

    return wrapper
