from json import JSONEncoder
from random import randrange

from networkx import draw_graphviz, write_dot

from graph import GH

graphviz_options = """
    node '[shape=circle, style=filled, nodesep = "1", labelangle="90"]';
    size="10,10";
    concentrate="true";
    repulsiveforce="0.2";
    overlap="prism";
    smoothing="spring";
    splines="true";
    edge='[len=3]';
    """


def output_json(filename):
    output = open(filename, 'w')

    data = [x for x in sorted(GH.nodes())]

    links = [{'source':data.index(source),
              'target': data.index(target),
              'value': 1}
             for source, target in sorted(GH.edges())[:100]]

    json_values = {'nodes': [{'nodename': x, 'group': randrange(5)}
                             for x in data],
                   'links': links}

    output.write(JSONEncoder().encode(json_values))
    output.close()


def output_dot(filename):
    draw_graphviz(GH)
    write_dot(GH, 'GH.dot')
