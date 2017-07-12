""" Utility functions for the Dagobah daemon. """

import logging
from datetime import date, datetime
import json
from functools import wraps
from sanic import response

try:
    from pymongo.objectid import ObjectId
except ImportError:
    try:
        from bson import ObjectId
    except ImportError:
        pass

from src.bus.exceptions import DagobahError, DAGValidationError


class DagobahEncoder(json.JSONEncoder):
    def default(self, obj):

        try:
            if isinstance(obj, ObjectId):
                return str(obj)
        except NameError:
            pass

        if isinstance(obj, datetime) or isinstance(obj, date):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class StrictJSONEncoder(json.JSONEncoder):
    def default(self, o):

        try:

            if isinstance(o, ObjectId):
                return str(o)

        except ImportError:
            pass

        if isinstance(o, datetime):
            return str(o)

        if isinstance(o, bytes):
            return str(o)

        return json.JSONEncoder.default(self, o)


def response_success(result):
    res = {'result': result, 'status': 200}
    return response.json(res)


def response_fail(result, status=400):
    res = {'result': result, 'status': status}
    return response.json(res, status=status)


def api_call(fn):
    """ Returns function result in API format if requested from an API
    endpoint """

    @wraps(fn)
    def wrapper(request):
        try:
            result = fn(request)
        except (DagobahError, DAGValidationError) as e:
            # Todo why this ?
            # if request and request.endpoint == fn.__name__:
            if request:
                return response.text(body=e.message, status=400)
            raise e
        except Exception as e:
            logging.exception(e)
            raise e

        if request and request.endpoint == fn.__name__:
            status_code = None
            try:
                if result and '_status' in result:
                    status_code = result['_status']
                    del result['_status']
            except TypeError:
                pass

            if isinstance(result, dict):
                if 'result' in result:
                    return response.json(body=result, status=status_code if status_code else 200)
                else:
                    return response.json(status=status_code if status_code else 200, body=result)
            else:
                return response.json(status=status_code if status_code else 200, body=result)

        else:
            return result

    return wrapper


def validate_dict(in_dict, **kwargs):
    """ Returns Boolean of whether given dict conforms to type specifications
    given in kwargs. """

    if not isinstance(in_dict, dict):
        raise ValueError('requires a dictionary')

    for key, value in kwargs.items():

        if key == 'required':
            for required_key in value:
                if required_key not in in_dict:
                    return False

        elif key not in in_dict:
            continue

        elif value == bool:

            in_dict[key] = (True
                            if str(in_dict[key]).lower() == 'true'
                            else False)

        else:

            if (isinstance(in_dict[key], list) and
                        len(in_dict[key]) == 1 and
                        value != list):
                in_dict[key] = in_dict[key][0]

            try:
                if key in in_dict:
                    in_dict[key] = value(in_dict[key])
            except ValueError:
                return False

    return True


def allowed_file(filename, extensions):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in [ext.lower()
                                                   for ext in extensions])
