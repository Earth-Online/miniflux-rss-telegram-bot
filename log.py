#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
module docs
"""

import logging
from logging import StreamHandler
from fluent import handler
from config import LOG_LEVEL, FLUENT_HOST, FLUENT_PORT
from fluent.handler import FluentRecordFormatter
from constant import LOGNAME

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',
  'type': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}

def init_log():

    logging.basicConfig(level=LOG_LEVEL)
    logger = logging.getLogger(LOGNAME)

    log_handler = None

    if FLUENT_HOST and FLUENT_PORT:
        log_handler = handler.FluentHandler(
            'rssbot', host=FLUENT_HOST, port=FLUENT_PORT)
        formatter = FluentRecordFormatter(custom_format)
    else:
        log_handler= StreamHandler()

    formatter = handler.FluentRecordFormatter(custom_format)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    log = logger



def get_logger():
    return logging.getLogger(LOGNAME)

log = get_logger()
