#coding:utf-8
import miniflux
import os
import logging

DEBUG = bool(os.environ.get('debug', True))


LOG_LEVEL = os.environ.get("log_level") or logging.INFO

HOST = os.environ.get('host') or '127.0.0.1'

PORT = os.environ.get('port') or '8080'

USERNAME = os.environ.get('username') or 'admin'

PASSWORD  = os.environ.get('password') or '123456'

TELEGRAPH_TOKEN = os.environ.get("telegraph")

WEBHOOK_URL = os.environ.get('webhook_url')

WEBHOOK_PORT = os.environ.get('webhook_port')

SENTRY_URL = os.environ.get('sentry')

FLUENT_HOST =  os.environ.get('fluent_host')

FLUENT_PORT = int(os.environ.get('fluent_port', '24224'))

TOKEN = os.environ.get('token')

DEFAULT_GET_NUM = 5

DEFAULT_PAGE_NUM = 5

DEFAULT_CHECK_TIME = 5*60

DEFAULT_SEND_LIMIE = 5

SERBER_ADDR = "http://{host}:{port}".format(host=HOST,port=PORT)

