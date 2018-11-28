#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from command import *
from help import help
from error import UserNotBindError
from client import cron_send
from cron import scheduler
from config import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

UPDATER = Updater(token=TOKEN)
DISPATCHER = UPDATER.dispatcher

START_HANDLER = CommandHandler('start', start)
BIND_HANDLER = CommandHandler('bind', bind, pass_args=True)
HELP_HANDLET = CommandHandler('help', help)
IMPORT_HANDLET = MessageHandler(Filters.document, import_feed)

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

if __name__ == "__main__":
    logging.info("bot run start ")
    UPDATER.start_polling()
    scheduler.add_job(cron_send,'interval',minutes=5)
    scheduler.start()
