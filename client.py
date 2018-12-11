# coding:utf-8
import telegram
import os
from typing import List
from module import DBSession
from module.user import User
from error import UserNotBindError, UserNotFoundError, UserOrPassError
from constant import EntryStatusRead, EntryStatusUnread
from miniflux import Client, ClientError
from config import (SERBER_ADDR, DEFAULT_PAGE_NUM, USERNAME,
                    PASSWORD, DEFAULT_SEND_LIMIE)
from send import format_feed, format_feeds

admin_client = Client(SERBER_ADDR, USERNAME, PASSWORD)


def new_client(user_id: str, session=DBSession) -> Client:
    session = session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    if user is None:
        raise UserNotBindError
        return
    return Client(SERBER_ADDR, username=user.username, password=user.password)


def bind_user(chat_id: str, username: str, password: str, session=DBSession):
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
    """
    调用需确保chat_id已绑定
    """
    session = session()
    user = session.query(User).filter(User.id == chat_id).first()
    session.close()
    return user.category_id


def change_categoryid(chat_id: str, category_id: str, session=DBSession):
    """
    """
    session = session()
    user = session.query(User).filter(User.id == chat_id).first()
    user.category_id = category_id
    session.commit()
    return user.category_id


def cron_send(bot, job, session=DBSession):
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


def send_entry(bot: telegram.Bot, user_id: str, entrys: List[dict]):
    for message in format_feeds(entrys):
        if message:
            bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=telegram.ParseMode.HTML)


def mark_read(client: Client, entrys: List[dict]) -> None:
    if not len(entrys):
        return
    ids = [entry['id'] for entry in entrys]
    client.update_entries(ids, EntryStatusRead)
