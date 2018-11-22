# coding:utf-8
import telegram
import os
from module import DBSession
from module.user import User
from error import UserNotBindError, UserNotFoundError, UserOrPassError
from constant import EntryStatusRead, EntryStatusUnread
from miniflux import Client, ClientError
from config import SERBER_ADDR


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
            ret = client.get_entries(status=EntryStatusUnread, limit=30)['entries']
        except ClientError as e:
            session.close()
            return
        TOKEN = os.environ.get('token')
        bot = telegram.Bot(token=TOKEN)
        for _ in ret:
            send_text = "{title} {url}".format(title=_['title'], url=_['url'])
            bot.send_message(chat_id=user.id, text=send_text)
        ids = [entry['id'] for entry in ret]
        try:
            client.update_entries(ids, EntryStatusRead)
        except ClientError as e:
            pass
    session.close()
