import functools
from typing import Callable
import logging
from error import UserNotBindError
from constant import *
from client import new_client, admin_client
from telegram.ext import CommandHandler
from miniflux import ClientError

global help_doc
help_doc = ''


def bot_function(arg_num=0, admin=False):
    def decorator(func):
        def wrapper(bot, update, args=[]):
            if len(args) < arg_num:
                bot.send_message(chat_id=update.message.chat_id, text=func.__doc__)
                return
            client = new_client(update.message.chat_id) if not admin else admin_client
            try:
                logging.debug(func.__name__)
                func(bot, update, args, client)
            except UserNotBindError:
                bot.send_message(chat_id=update.message.chat_id, text=NO_BIND_MSG)
        global help_doc
        if func.__doc__:
            help_doc = help_doc + func.__doc__
        return CommandHandler(func.__name__, wrapper, pass_args=bool(arg_num))
    return decorator

