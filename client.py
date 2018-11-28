# coding:utf-8
import telegram
import os
from typing import List
from module import DBSession
from module.user import User
from error import UserNotBindError, UserNotFoundError, UserOrPassError
from constant import EntryStatusRead, EntryStatusUnread
from miniflux import Client, ClientError
from config import SERBER_ADDR, DEFAULT_PAGE_NUM, USERNAME, PASSWORD

admin_client = miniflux.Client(SERBER_ADDR, USERNAME, PASSWORD)


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


def cron_send(session=DBSession):
    session = session()
    users = session.query(User).all()
    for user in users:
        client = Client(SERBER_ADDR, username=user.username,
                        password=user.password)

        try:
            ret = client.get_entries(
                status=EntryStatusUnread,
                limit=30)['entries']
        except ClientError as e:
            session.close()
            return
        TOKEN = os.environ.get('token')
        bot = telegram.Bot(token=TOKEN)
        send_entry(bot, user.id, ret)
        ids = [entry['id'] for entry in ret]
        try:
            client.update_entries(ids, EntryStatusRead)
        except ClientError as e:
            pass
    session.close()


def send_entry(bot: telegram.Bot, user_id: str, entrys: List[dict]):
    message = ""
    for index, value in zip(range(1, len(entrys)), entrys):
        send_text = "{title} <a>{url}</a> \n".format(
            title=value['title'], url=value['url'])
        message = message+send_text
        if index % DEFAULT_PAGE_NUM == 0:
            bot.send_message(
                chat_id=user_id, text=message,
                parse_mode=telegram.ParseMode.HTML)
            message = ""
    if message != '':
        bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode=telegram.ParseMode.HTML)


def mark_read(client: Client, entrys: List[dict]) -> None:
    ids = [entry['id'] for entry in entrys]
    client.update_entries(ids, EntryStatusRead)
    return
