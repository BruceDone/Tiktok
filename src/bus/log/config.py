# -*- coding: utf-8 -*-
import logging


def init_logger():
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    log = logging.getLogger()
    return log


logger = init_logger()
