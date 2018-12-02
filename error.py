# coding:utf-8
import logging
from constant import *
from miniflux import ClientError


class UserNotBindError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserOrPassError(Exception):
    pass


def error_handle(bot, update, error):
    try:
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
