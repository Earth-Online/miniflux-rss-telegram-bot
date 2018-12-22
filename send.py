#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from config import DEFAULT_PAGE_NUM, TELEGRAPH_TOKEN
from telegraph import Telegraph
from telegraph.exceptions import ParsingException, TelegraphException
from io import StringIO
from lxml import html
from log import log

feed_info_format = "id {id} title {title} site_url {site_url}"


def format_feed_info(feed):
    return feed_info_format.format(
        id=feed['id'],
        title=feed['title'],
        site_url=feed['site_url'])


def format_feeds_info(feeds):
    for i in range(0, len(feeds), DEFAULT_PAGE_NUM):
        send_text = ""
        for feed in feeds[i:i+DEFAULT_PAGE_NUM]:
            send_text = send_text + format_feed_info(feed)+"\n"
        yield send_text


user_info_format = "ID {id} 用户名 {username}"


def format_user_info(user):
    return user_info_format.format(id=user['id'], username=user['username'])


feed_format = """
{title}
■■■■■■■■■■■■■■■■■■
<a>{phurl}</a>
■■■■■■■■■■■■■■■■■■
<a>{url}</a>
■■■■■■■■■■■■■■■■■■
"""


def format_feed(feed):
    return feed_format.format(
        title=feed['title'],
        phurl=send_telegraph(feed),
        url=feed['url'])


def format_feeds(feeds):
    for feed in feeds:
        send_text = format_feed(feed)+"\n"
        yield send_text


category_info_format = 'id:{id} title:{title}\n'


def format_category_info(category):
    return category_info_format.format(
        id=category['id'],
        title=category['title'])


def fix_html(htmltext):

    htmlxml = html.fragments_fromstring(htmltext)
    for tag in htmlxml:
        # TODO if tag not have text.will error
        if isinstance(tag, str):
            continue
        if tag.tag in ['h1', 'h2', 'h5', 'h5']:
            tag.tag = "h4"
    ret = "".join([html.tostring(tag).decode("utf-8") if not isinstance(tag, str) else tag
                   for tag in htmlxml])
    return ret


def send_telegraph(feed):
    telegraph = Telegraph(TELEGRAPH_TOKEN)
    if not feed['content'].strip():
        return ''

    try:
        ret = telegraph.create_page(
            feed['title'], html_content=fix_html(feed['content']))
    except ParsingException as e:
        log.warning("url:"+feed['url']+" "+str(e)+fix_html(feed['content']))
        return ''
    except TelegraphException as e:
        log.warning("url:"+feed['url']+" "+str(e))
        return ''
    return 'https://telegra.ph/{}'.format(ret['path'])
