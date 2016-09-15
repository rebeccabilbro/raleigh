import os
import csv
import graph_tool.all as gt

from dateutil import parser
from datetime import datetime
from collections import namedtuple


DATA  = os.path.join(os.path.dirname(__file__), "data")
EMAIL = os.path.join(DATA, 'email_series.csv')


Email = namedtuple('Email', 'source, target, timestamp, subject')
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"


def parse_dataset(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row[2] = parser.parse(row[2])
            yield Email(*row)


def create_graph(path):
    g = gt.Graph(directed=False)

    # Property maps
    g.vp.email = g.new_vertex_property("string")
    g.ep.sent  = g.new_edge_property("object")
    g.ep.subject = g.new_edge_property("string")

    vmap = {}
    for row in parse_dataset(path):
        for addr in (row.source, row.target):
            if addr not in vmap:
                vmap[addr] = g.add_vertex()
                g.vp.email[vmap[addr]] = addr

        source = vmap[row.source]
        target = vmap[row.target]

        e = g.add_edge(source, target)
        g.ep.sent[e] = row.timestamp
        g.ep.subject[e] = row.subject


    return g


if __name__ == '__main__':

    g = create_graph(EMAIL)
    g.save("data/email_multigraph.gt")
