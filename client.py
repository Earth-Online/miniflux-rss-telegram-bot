# coding:utf-8
"""
miniflux client module
.. data:: ADMIN_CLIENT
    a miniflux admin Client

"""
import telegram
from telegram import Bot
from typing import List
from miniflux import Client, ClientError
from module import DBSession
from module.user import User
from error import UserNotBindError, UserOrPassError
from constant import EntryStatusRead, EntryStatusUnread
from config import (SERBER_ADDR, USERNAME,
                    PASSWORD, DEFAULT_SEND_LIMIE)
from send import format_feeds

ADMIN_CLIENT = Client(SERBER_ADDR, USERNAME, PASSWORD)


def new_client(user_id: str, session=DBSession) -> Client:
    """ from user_id get a miniflux client

    :param user_id: telegram chat_id
    :param session: database session class
    :type user_id: Union[int, str]
    :raise UserNotBindError: user not bind a miniflux account
    """
    session = session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    if user is None:
        raise UserNotBindError
    return Client(SERBER_ADDR, username=user.username, password=user.password)


def bind_user(chat_id: str, username: str, password: str, session=DBSession):
    """bind a telegram user and miniflux account

    :param chat_id: telegram chat_id
    :param username: miniflux account username
    :param password: miniflux account password
    :param session:  database session class
    :type chat_id: Union[int, str]
    :type username: str
    :type password: str
    :raise UserOrPassError: username or password error
    """
    session = session()
    client = Client(SERBER_ADDR, username=username, password=password)
    try:
        client.me()
    except ClientError:
        raise UserOrPassError
    ret = client.get_categories()
    category_id = ret[0]['id']
    user = User(
        id=chat_id,
        username=username,
        password=password,
        category_id=category_id)
    session.merge(user)
    session.commit()
    session.close()
    return


def get_categoryid(chat_id: str, session=DBSession):
    """ get a binded user default category id

    :param chat_id: telegram chat_id
    :type chat_id: Union[int, str]
    :rtype: int
    """
    session = session()
    user = session.query(User).filter(User.id == chat_id).first()
    session.close()
    return user.category_id


def change_categoryid(chat_id: str, category_id: str, session=DBSession):
    """change a user default category id

    :param chat_id: telegram chat_id
    :type chat_id: Union[int, str]
    :param category_id: change to category_id
    :type category_id: Union[int, str]
    """
    session = session()
    user = session.query(User).filter(User.id == chat_id).first()
    user.category_id = category_id
    session.commit()
    return user.category_id


def cron_send(bot, job, session=DBSession):
    """cron_send

    :param bot: telegram bot
    :param job: telegram job queue
    :param session:
    """
    session = session()
    users = session.query(User).all()
    for user in users:
        client = Client(SERBER_ADDR, username=user.username,
                        password=user.password)

        try:
            ret = client.get_entries(
                status=EntryStatusUnread,
                limit=DEFAULT_SEND_LIMIE)['entries']
        except ClientError as e:
            continue

        send_entry(bot, user.id, ret)
        mark_read(client, ret)
    session.close()


def send_entry(bot: telegram.Bot, user_id: int, entrys: List[dict]):
    """send_entry

    :param bot:
    :type bot: Bot
    :param Bot:
    :param user_id:
    :type user_id: int
    :param entrys:
    :type entrys: List[dict]
    """
    for message in format_feeds(entrys):
        if message:
            bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=telegram.ParseMode.HTML)


def mark_read(client: Client, entrys: List[dict]) -> None:
    """mark some entrys to readed

    :param client: miniflux client
    :param entrys: miniflux entrys
    :type client: Client
    """
    if not len(entrys):
        return
    ids = [entry['id'] for entry in entrys]
    client.update_entries(ids, EntryStatusRead)
