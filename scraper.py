from json import JSONDecoder
from urllib2 import urlopen
from pprint import PrettyPrinter


latest_commits = []
pp = PrettyPrinter()
base_url = "http://github.com/api/v2/json"


def data_parse(resp, key):
    try:
        resp_json = JSONDecoder().decode(resp.read())
        return resp_json[key]
    except:
        return []


def get_top_repos(search_term):
    s = base_url + "/repos/search/%s?fork=false"
    resp = urlopen(s % search_term)
    resp_json = JSONDecoder().decode(resp.read())
    return [(x.get('id'), x.get('username'), x.get('name'))
            for x in resp_json['repositories']]


def get_latest_commit(user, repo):
    query = base_url + "/commits/list/%s/%s/master" % (user, repo)
    resp = urlopen(query)
    key = 'commits'
    return data_parse(resp, key)


def get_user_following(user):
    query = base_url + "/user/show/%s/following" % user
    resp = urlopen(query)
    key = 'users'
    return data_parse(resp, key)


def get_user_followers(user):
    query = base_url + "/user/show/%s/followers" % user
    resp = urlopen(query)
    key = 'users'
    return data_parse(resp, key)

