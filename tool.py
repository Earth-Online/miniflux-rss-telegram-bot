"""
tool functool
"""
import functools
from typing import Callable, List, Text, SupportsInt, Any
from telegram.ext import CommandHandler
from requests.exceptions import RequestException
import logging
from module import DBSession
from module.user import User
from functools import wraps
from error import UserNotBindError
from constant import *
from client import new_client, ADMIN_CLIENT
from telegram.ext import CommandHandler
from miniflux import ClientError

global help_doc
help_doc = ''


def command_wrap(name: Text = None, *args, **kwargs):
    """
    commandHandler wrap
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return CommandHandler(name or func.__name__,
                              callback=wrapper, **kwargs)
    return decorator


def check_args(num: int = 0, default: List[Any] = []):
    """
    check command arg num decorator
    """
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, *args, **kwargs):

            arg = kwargs.get("args")
            if len(arg) < len(default):
                for idx, value in enumerate(default):
                    idx = idx+1
                    if not value and len(arg) < idx:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text=func.__doc__)
                        return
                    if value and len(arg) < idx:
                        kwargs['args'].append(value)
            if len(arg) < num:
                bot.send_message(
                     chat_id=update.message.chat_id,
                     text=func.__doc__)
                return
            return func(bot, update,  *args, **kwargs)
        return wrapper
    return decorator


def check_bind(func: Callable):
    """
    check user bind a account decorator. if not will send error msg
    """
    @wraps(func)
    def wrapper(bot, update, *args, **kwargs):
        session = DBSession()
        user = session.query(User).filter(
            User.id == update.message.chat_id).first()
        session.close()
        if user is None:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=NO_BIND_MSG)
            return
        return func(bot, update,  *args, **kwargs)
    return wrapper


def send_text(func: Callable):
    """
    send ret text to user decorator
    """
    @wraps(func)
    def wrapper(bot, update, *args, **kwargs):
        ret = func(bot, update,  *args, **kwargs)
        if ret:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=ret)
        return ret
    return wrapper


def get_client(admin: bool = False):
    """
    get a miniflux client decorator
    """
    def decorator(func):
        @wraps(func)
        def wrapper(bot, update, *args, **kwargs):
            try:
                client = new_client(
                    update.message.chat_id) if not admin else ADMIN_CLIENT
                return func(bot, update, client=client, *args, **kwargs)
            except UserNotBindError:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=NO_BIND_MSG)
                return
            except ClientError as e:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=e.get_error_reason())
                return
            except RequestException as e:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=str(e))
                return

        return wrapper
    return decorator
