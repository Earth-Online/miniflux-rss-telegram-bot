#!/usr/bin/python
# -*- coding: utf-8 -*-

feed_info_format =  "id {id} title {title}"

def format_feed_info(feed):
    return feed_info_format.format(id=feed['id'], title=feed['title'])


user_info_format = "ID {id} 用户名 {username}"

def format_user_info(user):
    return user_info_format.format(id=user['id'], username=user['username'])
