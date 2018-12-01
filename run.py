#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
from command import *
from help import help
from error import UserNotBindError
from client import cron_send
from config import TOKEN, DEFAULT_CHECK_TIME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

UPDATER = Updater(token=TOKEN)
DISPATCHER = UPDATER.dispatcher
JOB = UPDATER.job_queue

START_HANDLER = CommandHandler('start', start)
BIND_HANDLER = CommandHandler('bind', bind, pass_args=True)
HELP_HANDLET = CommandHandler('help', help)
IMPORT_HANDLET = MessageHandler(Filters.document, import_feed)
URL_HANDLER = MessageHandler(
    Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK),
    url_handle)

DISPATCHER.add_handler(URL_HANDLER)
DISPATCHER.add_handler(START_HANDLER)
DISPATCHER.add_handler(BIND_HANDLER)
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

JOB.run_repeating(cron_send, interval=DEFAULT_CHECK_TIME, first=0)

if __name__ == "__main__":
    logging.info("bot run start ")
    UPDATER.start_polling()
    UPDATER.idle()
