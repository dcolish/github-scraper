from ConfigParser import SafeConfigParser
import logging
from time import sleep

from couchdb import Database

from graph import me, select_user
from scraper import (
    get_user_followers,
    get_user_following,
)


conf = SafeConfigParser()
db = Database(conf.get('db', 'remote'))
max_depth = 10
conf.read('auth.cfg')
logging.basicConfig(level=logging.DEBUG)


def crawl_user(user, depth=0):
    followers = get_user_followers(user)
    following = get_user_following(user)

    if not db.query(select_user % user):
        db.save({'user': user, 'followers': followers, 'following': following})

    for follower in followers:
        if depth < max_depth:
            sleep(5)
            crawl_user(follower, depth + 1)

    for follow in following:
        if depth < max_depth:
            sleep(5)
            crawl_user(follow, depth + 1)


if __name__ == "__main__":
    crawl_user(me)
