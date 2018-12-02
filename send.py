#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import DEFAULT_PAGE_NUM

feed_info_format = "id {id} title {title}"


def format_feed_info(feed):
    return feed_info_format.format(id=feed['id'], title=feed['title'])

def format_feeds_info(feeds):
    for i in range(0, len(feeds), DEFAULT_PAGE_NUM):
        send_text = ""
        for feed in feeds[i:DEFAULT_PAGE_NUM]:
            send_text = send_text + format_feed_info(feed)+"\n"
        yield send_text


user_info_format = "ID {id} 用户名 {username}"


def format_user_info(user):
    return user_info_format.format(id=user['id'], username=user['username'])


feed_format = "{title} <a>{url}</a>\n"


def format_feed(feed):
    return feed_format.format(title=feed['title'], url=feed['url'])

def format_feeds(feeds):
    for i in range(0, len(feeds), DEFAULT_PAGE_NUM):
        send_text = ""
        for feed in feeds[i:DEFAULT_PAGE_NUM]:
            send_text = send_text + format_feed(feed)+"\n"
        yield send_text

category_info_format = 'id:{id} title:{title}\n'


def format_category_info(category):
    return category_info_format.format(
        id=category['id'],
        title=category['title'])
