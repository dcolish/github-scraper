from ConfigParser import SafeConfigParser
import logging

from couchdb import Database
from networkx import Graph

conf = SafeConfigParser()
conf.read('auth.cfg')
logging.basicConfig(level=logging.DEBUG)

GH = Graph(name="Github")
me = 'dcolish'
max_depth = 10
db = Database(conf.get('db', 'remote'))

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


def graph_user(user, depth=0):
    logging.debug("Searching for %s", user)
    logging.debug("At depth %d", depth)
    followers = following = []
    result = [x.value for x in db.query(select_user % user)]

    if result:
        result = result.pop()
        following = result['following']
        followers = result['followers']

    if not GH.has_node(user):
        logging.debug("Adding %s to graph", user)
        GH.add_node(user)

    for follower in followers:
        if not GH.has_node(follower):
            GH.add_node(follower)
            logging.debug("Adding %s to graph", follower)
            if depth < max_depth:
                graph_user(follower, depth + 1)
        GH.add_edge(follower, user, {'weight': 2})

    for follow in following:
        if not GH.has_node(follow):
            GH.add_node(follow)
            logging.debug("Adding %s to graph", follow)
            if depth < max_depth:
                graph_user(follow, depth + 1)

        if GH.has_edge(follow, user):
            GH[follow][user]['weight'] += 1
        else:
            GH.add_edge(user, follow, {'weight': 1})


if __name__ == "__main__":
    graph_user(me)
