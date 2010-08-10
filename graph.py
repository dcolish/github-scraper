# from json import JSONEncoder
# from random import randrange
from ConfigParser import SafeConfigParser
from couchdb import Database
from time import sleep
from networkx import Graph
import networkx as nx

from scraper import (
    get_latest_commit,
    get_user_followers,
    get_user_following,
    get_top_repos,
)
conf = SafeConfigParser()
conf.read('auth.cfg')

GH = Graph(name="Github")
me = 'dcolish'
max_depth = 10
db = Database(conf.get('db', 'db_url'))

select_all = """
function (doc) {
   emit(doc.user, doc.followers, doc.following);
}
"""

select_user = """
function (doc) {
  if (doc.user == "%s") {
    emit(null,
         {user: doc.user, followers: doc.followers, following: doc.following});
  }
}
"""


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


def graph_user(user, depth=0):
    followers = following = []
    result = [x.value for x in db.query(select_user % user)]

    if result:
        result = result.pop()
        following = result['following']
        followers = result['followers']

    if not GH.has_node(user):
        GH.add_node(user)

    for follower in followers:
        if not GH.has_node(follower):
            GH.add_node(follower)
            graph_user(follower, depth + 1)
        GH.add_edge(follower, user, {'weight': 2})

    for follow in following:
        if not GH.has_node(follow):
            GH.add_node(follow)
            graph_user(follower, depth + 1)

        if GH.has_edge(follow, user):
            GH[follow][user]['weight'] += 1
        else:
            GH.add_edge(user, follow, {'weight': 1})


if __name__ == "__main__":
    crawl_user(me)

    # graph_user(me)
    # nx.draw_graphviz(GH)
    # nx.write_dot(GH, 'GH.dot')

    # output = open('data.js', 'w')

    # data = [x for x in sorted(GH.nodes())]

    # links = [{'source':data.index(source),
    #           'target': data.index(target),
    #           'value': 1}
    #          for source, target in sorted(GH.edges())[:100]]

    # json_values = {'nodes': [{'nodename': x, 'group': randrange(5)}
    #                          for x in data],
    #                'links': links}

    # output.write(JSONEncoder().encode(json_values))
    # output.close()
