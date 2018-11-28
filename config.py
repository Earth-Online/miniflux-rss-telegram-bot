#coding:utf-8
import miniflux
import os

HOST = os.environ.get('host') or '127.0.0.1'

PORT = os.environ.get('port') or '8080'

USERNAME = os.environ.get('username') or 'admin'

PASSWORD  = os.environ.get('password') or '123456'

TOKEN = os.environ.get('token')

DEFAULT_GET_NUM = 5

DEFAULT_PAGE_NUM = 5

SERBER_ADDR = "http://{host}:{port}".format(host=HOST,port=PORT)
