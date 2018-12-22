# coding:utf-8
import io
import telegram
from inspect import *
from client import new_client
from tool import (command_wrap, check_args, send_text,
                  get_client, check_bind)
from constant import *
from telegram import InputFile, MessageEntity
from client import (new_client, bind_user, get_categoryid,
                    change_categoryid, send_entry, mark_read)
from module import DBSession
from module.user import User
from config import DEFAULT_GET_NUM
from miniflux import ClientError
from error import UserNotBindError, UserOrPassError
from send import format_feed_info, format_user_info, format_category_info, format_feeds_info


@command_wrap()
@send_text
def start(bot, update):
    """
    """
    return START_MSG


@command_wrap(pass_args=True)
@check_args(num=2)
@send_text
def bind(bot, update, args):
    """
    bind - args:<username> <password> bind your account
    """
    try:
        bind_user(update.message.chat_id, *args)
    except UserOrPassError:
        return USER_OR_PASS_ERROE_MSG
    return BIND_OK_MSG


@command_wrap(pass_args=True)
@check_args(num=2)
@get_client(admin=True)
def new_user(bot, update, args, client):
    """
    new_user - arg <username> <password> create new account and bind
    """
    client.create_user(args[0], args[1], False)
    return CREATE_OK_MSG


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@send_text
def change_default_categoryid(bot, update, args):
    """
    change_default_categoryid - arg <categoryid> change default categoryid
    """
    change_categoryid(update.message.chat_id, args[0])
    return UPDATE_OK_MSG


@command_wrap()
@check_bind
@send_text
def get_default_categoryid(bot, update):
    """
    get_default_categoryid - get default category_id
    """
    category_id = get_categoryid(update.message.chat_id)
    return category_id


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def add_feed(bot, update, args, client):
    """
    add_feed - arg <url> [category_id]  add a feed
    """
    category_id = args[1] if len(
        args) > 1 else get_categoryid(update.message.chat_id)
    if not str(category_id).isdecimal():
        bot.send_message(
            chat_id=update.message.chat_id,
            text=ID_NO_INT_MSG)
        return
    client.create_feed(args[0], category_id, crawler=True)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)


def import_feed(bot, update):
    """
    发送opml文件将会导入
    """
    if update.message.document.file_name.split('.')[-1] != 'opml':
        return
    client = new_client(update.message.chat_id)
    file_id = update.message.document.file_id
    newFile = bot.get_file(file_id)
    data = newFile.download_as_bytearray()
    client.import_feeds(data)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)


@command_wrap()
@check_bind
@get_client()
def export(bot, update, client):
    """
    export - export yous feed to a file
    """
    _ = client.export()
    opml_file = io.BytesIO(bytes(_, 'utf-8'))
    bot.send_document(
        chat_id=update.message.chat_id,
        document=opml_file,
        filename="export.opml")
    opml_file.close()


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def discover(bot, update, args, client):
    """
    discover - arg <url>  try discover a site feed address and add
    """
    ret = client.discover(args[0])
    category_id = get_categoryid(update.message.chat_id)
    client.create_feed(ret[0]['url'], category_id, crawler=True)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)


@command_wrap(pass_args=True)
@check_bind
@check_args(default=[DEFAULT_GET_NUM])
@get_client()
def get_entries(bot, update, args, client):
    """
    get_entries - arg <num>  get yous feed new post
    """
    num = args[0]
    ret = client.get_entries(limit=num , status=EntryStatusUnread)
    if not len(ret['entries']):
        bot.send_message(chat_id=update.message.chat_id, text=NO_INFO_MSG)
        return
    send_entry(bot, update.message.chat_id, ret['entries'])
    mark_read(client, ret['entries'])


@command_wrap()
@check_bind
@get_client()
def me(bot, update, client):
    """
    me - get yous account info
    """
    ret = client.me()
    ret_text = format_user_info(ret)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
@send_text
def delete_feed(bot, update, args, client):
    """
    delete_feed - arg <feed_id> delete a feed
    """
    client.delete_feed(args[0])
    return DELETE_OK_MSG


@command_wrap()
@check_bind
@get_client()
def get_categories(bot, update, client):
    """
    get_categories - get yous categories
    """
    ret = client.get_categories()
    ret_text = ''
    for i in ret:
        ret_text = ret_text + format_category_info(i)
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def create_category(bot, update, args, client):
    """
    create_categories - arg <title> create category
    """
    ret = client.create_category(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=CREATE_OK_MSG)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def delete_category(bot, update, args, client):
    """
    delete_category - args <id> delete a category
    """
    ret = client.delete_category(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_OK_MSG)


@command_wrap()
@check_bind
@get_client()
def delete_user(bot, update,client):
    """
    delete_user - delete your user
    """
    user_id = client.me()['id']
    ret = admin_client.delete_user(user_id)
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_OK_MSG)


@command_wrap()
@check_bind
@get_client()
def get_feeds(bot, update, client):
    """
    get_feeds - get yous feed info
    """
    ret = client.get_feeds()
    for _ in format_feeds_info(ret):
        bot.send_message(chat_id=update.message.chat_id,
                         text=_)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def get_feed(bot, update, args, client):
    """
    get_feed - arg <feed_id>; get feed_id feed info
    """
    ret = client.get_feed(args[0])
    bot.send_message(
        chat_id=update.message.chat_id,
        text=format_feed_info(ret))


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def refresh_feed(bot, update, args, client):
    """
    refresh - arg <feed_id> refresh feed_id feed
    """
    ret = client.refresh_feed(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=REFRESH_OK_MSG)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1, default=[None, DEFAULT_GET_NUM])
@get_client()
def get_feed_entries(bot, update, args, client):
    """
    get_feed_entries - arg <feed_id> [num]
    """
    num = args[1]
    ret = client.get_feed_entries(
        args[0],
        limit=num,
        status=EntryStatusUnread)
    send_entry(bot, update.message.chat_id, ret['entries'])
    mark_read(client, ret['entries'])


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def bookmark(bot, update, args, client):
    """
    bookmark - arg <id> bookmark
    """
    ret = client.toggle_bookmark(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=MARK_OK_MSG)


@command_wrap(pass_args=True)
@check_bind
@check_args(num=1)
@get_client()
def update_category(bot, update, args, client):
    """
    update_category - args <category_id> <title>
    """
    ret = client.update_category(args[0], args[1])
    bot.send_message(chat_id=update.message.chat_id, text=UPDATE_OK_MSG)

@check_bind
@get_client()
def url_handle(bot, update, client):
    category_id = get_categoryid(update.message.chat_id)
    for url in update.message.parse_entities(types=MessageEntity.URL).values():
        client.create_feed(update.message.text, category_id)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)
