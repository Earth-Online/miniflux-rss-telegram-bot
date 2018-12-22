# coding:utf-8
"""
error class
"""
import logging
from constant import *
from miniflux import ClientError
from telegram import Bot, Update
from log import log


class UserNotBindError(Exception):
    """
    user not bind a miniflux account
    """
    pass


class UserNotFoundError(Exception):
    """
    not found this user
    """
    pass


class UserOrPassError(Exception):
    """
    miniflux account or password error
    """
    pass


def error_handle(bot, update, error):
    """telegram bot errror handle

    :param bot: telegram Bot Instance
    :param update: telegram Update Instance
    :param error:  code error
    :type error: Exception
    :type update: Update
    :type bot:  Bot
    """
    try:
        log.error(error)
        raise error
    except UserOrPassError:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=USER_OR_PASS_ERROE_MSG)
    except UserNotBindError:
        bot.send_message(chat_id=update.message.chat_id, text=NO_BIND_MSG)
    except ClientError as error:
        logging.debug(error.get_error_reason())
        bot.send_message(
            chat_id=update.message.chat_id,
            text=error.get_error_reason())
    except UserNotBindError:
        bot.send_message(chat_id=update.message.chat_id, text=NO_BIND_MSG)
