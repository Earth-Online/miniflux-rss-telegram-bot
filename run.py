#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import sentry_sdk
from sentry_sdk import configure_scope
from requests.exceptions import RequestException
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
from command import *
from help import help
from log import init_log, get_logger
from error import UserNotBindError, error_handle
from client import cron_send
from config import (TOKEN, DEFAULT_CHECK_TIME, LOG_LEVEL, TELEGRAPH_TOKEN,
                    DEBUG, SENTRY_URL)
from constant import NO_TOKEN_MSG, SERVER_ERROR, ADMIN_ERROR, SENTRY_OPEN
from client import ADMIN_CLIENT
from miniflux import ClientError


def init():
    """
    check config
    """
    init_log()
    log = get_logger()
    if not (TOKEN and TELEGRAPH_TOKEN):
        log.error(NO_TOKEN_MSG)
        exit()

    try:
        ADMIN_CLIENT.me()
    except ClientError:
        log.error(ADMIN_ERROR)
        exit()
    except RequestException:
        log.error(SERVER_ERROR)
        exit()

    if not DEBUG:
        log.info("not debug")
        if SENTRY_URL:
            log.info(SENTRY_OPEN)
            with configure_scope() as scope:
                scope.user = {"id": TOKEN.split(":"[0])}
            sentry_sdk.init(SENTRY_URL)


def main():
    init()
    UPDATER = Updater(token=TOKEN, request_kwargs={"read_timeout": 30},)
    DISPATCHER = UPDATER.dispatcher
    JOB = UPDATER.job_queue

    HELP_HANDLET = CommandHandler('help', help)
    IMPORT_HANDLET = MessageHandler(Filters.document, import_feed)
    URL_HANDLER = MessageHandler(
        Filters.entity(MessageEntity.URL),
        url_handle)
    log = get_logger()
    DISPATCHER.add_handler(start)
    DISPATCHER.add_handler(bind)
    DISPATCHER.add_handler(new_user)
    DISPATCHER.add_handler(add_feed)
    DISPATCHER.add_handler(export)
    DISPATCHER.add_handler(discover)
    DISPATCHER.add_handler(get_entries)
    DISPATCHER.add_handler(HELP_HANDLET)
    DISPATCHER.add_handler(me)
    DISPATCHER.add_handler(delete_feed)
    DISPATCHER.add_handler(get_categories)
    DISPATCHER.add_handler(create_category)
    DISPATCHER.add_handler(delete_category)
    DISPATCHER.add_handler(delete_user)
    DISPATCHER.add_handler(IMPORT_HANDLET)
    DISPATCHER.add_handler(get_feeds)
    DISPATCHER.add_handler(get_feed)
    DISPATCHER.add_handler(refresh_feed)
    DISPATCHER.add_handler(update_category)
    DISPATCHER.add_handler(get_feed_entries)
    DISPATCHER.add_handler(bookmark)
    DISPATCHER.add_handler(get_default_categoryid)
    DISPATCHER.add_handler(change_default_categoryid)
    DISPATCHER.add_handler(URL_HANDLER)
    DISPATCHER.add_error_handler(error_handle)
    JOB.run_repeating(cron_send, interval=DEFAULT_CHECK_TIME, first=0)
    log.info("bot run start ")
    UPDATER.start_polling()
    UPDATER.idle()


if __name__ == "__main__":
    main()
