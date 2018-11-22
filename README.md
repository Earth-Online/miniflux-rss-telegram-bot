## miniflux-rss-telegram-bot

![Docker Build Status](https://img.shields.io/docker/build/bluebird1/miniflux-rss-telegram-bot.svg)
![Docker Automated build](https://img.shields.io/docker/automated/bluebird1/miniflux-rss-telegram-bot.svg)
[![Build Status](https://travis-ci.org/blue-bird1/miniflux-rss-telegram-bot.svg?branch=master)](https://travis-ci.org/blue-bird1/miniflux-rss-telegram-bot)
[![Coverage Status](https://coveralls.io/repos/github/blue-bird1/miniflux-rss-telegram-bot/badge.svg)](https://coveralls.io/github/blue-bird1/miniflux-rss-telegram-bot)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fblue-bird1%2Fminiflux-rss-telegram-bot.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fblue-bird1%2Fminiflux-rss-telegram-bot?ref=badge_shield)

Telegram rss robot supported by miniflux

### Requirements
`python>3.4`
`miniflux`

### install
#### docker
edit .env file
`docker run --env-file=.env -d bluebird1/miniflux-rss-telegram-bot`
#### docker-compose
edit .env file
`docker-compose up -d`

`docker exec -ti rssbot_miniflux_1  /usr/local/bin/miniflux -migrate`

`docker exec -ti rssbot_miniflux_1  /usr/local/bin/miniflux  -create-admin` # need like .env username password
#### python
```bash
# pip -r requirements.txt
# export token <you bot token>
# export host <you miniflux host>
# export port <you miniflux por>
# export username <you miniflux admin username>
# export password <you miniflux admin password>
# python run.py
```

### use bot
```
/new_user  <username> <password> #create you account
/bind <username> <password> #bind you account
/discover <url> # try auto discover rss feed
/add_feel <feedurl> <category_id> # add feed
/export # export you feed
/get_entries  <num> # get rss
```

auto print help
```
    usage: /new_user username password
    
    usage: /addfeed url category_id
    
    usage: /export
    
    usage: /discover url
    
    usage: /get_entries num
    
    usage: /me
    
    usage: /delete_feed <feed_id>
    
    usage: /get_categories
    
    usage: /create_categories title
    
    usage: /delete_category id
    
    usage: /delte_user
    
    usage:/get_feeds
    
    usage:/get_feed feed_id
    
    usage:/refresh_feed feed_id
    
    usage:/get_feed_entries feed_id num
    
    usage:/bookmark id
    
    usage:/update_category category_id title
    
    usage: /bind username password
    
    发送opml文件将会导入
    
    欢迎使用rss机器人,使用/help获取更多帮助
```

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fblue-bird1%2Fminiflux-rss-telegram-bot.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fblue-bird1%2Fminiflux-rss-telegram-bot?ref=badge_large)
