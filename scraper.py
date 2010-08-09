from json import JSONDecoder
from urllib2 import urlopen
from pprint import PrettyPrinter


latest_commits = []
pp = PrettyPrinter()
base_url = "http://github.com/api/v2/json"
search_term = "python"
s = base_url + "/repos/search/%s?fork=false"
resp = urlopen(s % search_term)
resp_json = JSONDecoder().decode(resp.read())
repoids = [(x.get('id'), x.get('username'), x.get('name'))
           for x in resp_json['repositories']]


def get_latest_commit(user, repo):
    query = base_url + "/commits/list/%s/%s/master" % (user, repo)
    resp = urlopen(query)
    resp_json = JSONDecoder().decode(resp.read())
    return resp_json['commits'][0]

latest_commits = [get_latest_commit(user, repo)
                  for repoid, user, repo in repoids]

pp.pprint([x['message'] for x in latest_commits])
