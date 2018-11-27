# coding:utf-8
import io
import telegram
from inspect import *
from client import new_client
from tool import bot_function, mark_read
from constant import *
from telegram import InputFile
from client import (new_client, bind_user, get_categoryid,
                    change_categoryid, send_entry)
from module import DBSession
from module.user import User
from config import admin_client
from miniflux import ClientError
from error import UserNotBindError, UserOrPassError


def start(bot, update):
    """
    欢迎使用rss机器人,使用/help获取更多帮助
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text=getdoc(
            globals()[
                getframeinfo(
                    currentframe()).function]))


def bind(bot, update, args):
    """
    bind - args:<username> <password> bind your account
    """
    if len(args) != 2:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=getdoc(
                globals()[
                    getframeinfo(
                        currentframe()).function]))
        return
    try:
        bind_user(update.message.chat_id, *args)
        bot.send_message(chat_id=update.message.chat_id, text=BIND_OK_MSG)
    except UserOrPassError:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=USER_OR_PASS_ERROE_MSG)


@bot_function(arg_num=2, admin=True)
def new_user(bot, update, args, client):
    """
    new_user - arg <username> <password> create new account
    """
    client.create_user(args[0], args[1], False)
    bot.send_message(chat_id=update.message.chat_id, text=CREATE_OK_MSG)


@bot_function(arg_num=1)
def change_default_categoryid(bot, update, args,  _):
    """
    change_default_categoryid - arg <categoryid> change default categoryid
    """
    change_categoryid(update.message.chat_id, args[0])
    bot.send_message(chat_id=update.message.chat_id, text=UPDATE_OK_MSG)


@bot_function(arg_num=0)
def get_default_categoryid(bot, update, args,  _):
    """
    get_default_categoryid - get default category_id
    """
    category_id = get_categoryid(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=category_id)


@bot_function(arg_num=1)
def add_feed(bot, update, args, client):
    """
    addfeed - arg <url> [category_id]  add a feed
    """
    category_id = None
    if len(args) == 1:
        category_id = get_categoryid(update.message.chat_id)
    else:
        category_id = args[1]
        if not category_id.isdecimal():
            bot.send_message(
                chat_id=update.message.chat_id,
                text=ID_NO_INT_MSG)
            return
    client.create_feed(args[0], category_id)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)


def import_feed(bot, update):
    """
    发送opml文件将会导入
    """
    if not update.document.file_name.split('.')[-1] != 'opml':
        return
    try:
        client = new_client(update.message.chat_id)
    except UserNotBindError:
        bot.send_message(chat_id=update.message.chat_id, text=NO_BIND_MSG)
        return

    file_id = update.message.document.file_id
    newFile = bot.get_file(file_id)
    data = newFile.download_as_bytearray()
    try:
        client.import_feeds(data.decode())
    except ClientError as error:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=error.get_error_reason())
        return


@bot_function(arg_num=0)
def export(bot, update, _, client):
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


@bot_function(arg_num=1)
def discover(bot, update, args, client):
    """
    discover - arg <url>  try discover a site feed address and add
    """
    ret = client.discover(args[0])
    category_id = get_categoryid(update.message.chat_id)
    client.create_feed(ret[0]['url'], category_id)
    bot.send_message(chat_id=update.message.chat_id, text=ADD_FEED_OK_MSG)


@bot_function(arg_num=0)
def get_entries(bot, update, args, client):
    """
    get_entries - arg <num>  get yous feed new post
    """
    num = 5
    if len(args):
        num = args[0]
    ret = client.get_entries(limit=num, status=EntryStatusUnread)
    send_entry(bot, update.message.chat_id, ret['entries'])
    mark_read(client, ret['entries'])


@bot_function(arg_num=0)
def me(bot, update, args, client):  # pylint:disable=invalid-name,unused-argument
    """
    me - get yous account info
    """
    ret = client.me()
    ret_text = '''
     ID {} 用户名 {}
    '''.format(ret['id'], ret['username'])
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@bot_function(arg_num=1)
def delete_feed(bot, update, args, client):
    """
    delete_feed - arg <feed_id> delete a feed
    """
    client.delete_feed(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_FEED_OK_MSG)


@bot_function(arg_num=0)
def get_categories(bot, update, _, client):
    """
    get_categories - get yous categories
    """
    ret = client.get_categories()
    ret_text = ''
    for i in ret:
        ret_text = ret_text + 'id:{} title:{}\n'.format(i['id'], i['title'])
    bot.send_message(chat_id=update.message.chat_id, text=ret_text)


@bot_function(arg_num=1)
def create_category(bot, update, args, client):
    """
    create_categories - arg <title> create category
    """
    ret = client.create_category(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=CREATE_OK_MSG)


@bot_function(arg_num=1)
def delete_category(bot, update, args, client):
    """
    delete_category - args <id> delete a category
    """
    ret = client.delete_category(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_OK_MSG)


@bot_function(arg_num=0)
def delete_user(bot, update, _, client):
    """
    delete_user - delete your user
    """
    user_id = client.me()['id']
    ret = admin_client.delete_user(user_id)
    bot.send_message(chat_id=update.message.chat_id, text=DELETE_OK_MSG)


@bot_function(arg_num=0)
def get_feeds(bot, update, _, client):
    """
    get_feeds - get yous feed info
    """
    ret = client.get_feeds()
    for _ in ret:
        bot.send_message(chat_id=update.message.chat_id,
                         text="id {} title {}\n".format(_['id'], _['title']))


@bot_function(arg_num=1)
def get_feed(bot, update, args, client):
    """
    get_feed - arg <feed_id>; get feed_id feed info
    """
    ret = client.get_feed(args[0])
    bot.send_message(
        chat_id=update.message.chat_id,
        text="url {} title {}\n".format(
            ret['site_url'],
            ret['title']))


@bot_function(arg_num=1)
def refresh_feed(bot, update, args, client):
    """
    refresh - arg <feed_id> refresh feed_id feed
    """
    ret = client.refresh_feed(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=REFRESH_OK_MSG)


@bot_function(arg_num=2)
def get_feed_entries(bot, update, args, client):
    """
    get_feed_entries - arg <feed_id> <num>
    """

    ret = client.get_feed_entries(
        args[0],
        limit=args[1],
        status=EntryStatusUnread) 
    send_entry(bot, update.message.chat_id, ret['entries'])
    mark_read(client, ret['entries'])


@bot_function(arg_num=1)
def bookmark(bot, update, args, client):
    """
    bookmark - arg <id> bookmark
    """
    ret = client.toggle_bookmark(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=MARK_OK_MSG)


@bot_function(arg_num=2)
def update_category(bot, update, args, client):
    """
    update_category - args <category_id> <title>
    """
    ret = client.update_category(args[0], args[1])
    bot.send_message(chat_id=update.message.chat_id, text=UPDATE_OK_MSG)
