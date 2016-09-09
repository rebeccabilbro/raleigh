#!/usr/bin/env python3
# sklearn_graph.py

# Author:        Rebecca Bilbro <rebecca.bilbro@bytecubed.com>
# Title:         Visualizing Scikit-Learn Contributions on Github over Time
# Description:
# Two types of nodes - commit and contributor nodes.
# Contributors have edges to one or more commit vertices,
# where the time weight is the delta from the contributor's last commit.
# Commits have an edge to their parent,
# whose time weight is the delta between their commit timestamps.

#############################################################################
# Imports
#############################################################################

import os
import csv
import networkx as nx
import matplotlib.pyplot as plt

from functools import partial
from datetime import datetime
from operator import itemgetter
from collections import namedtuple


#############################################################################
# Fixtures
#############################################################################

DATA       = os.path.join(os.path.dirname(__file__), 'data')
INPATH     = os.path.join(DATA, 'sklearncommits.txt')
IMGPATH    = 'sklearngraph.png'
GRAPHML    = 'sklearngraph.graphml'

DATEFORMAT       = '%a %b %d %H:%M:%S %Y %z'
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"

Commit = namedtuple('Commit', 'commit, parents, contributor, timestamp, elapsed')


def parse_dataset(path):
    """
    Reads the data set and yields parsed tuples
    """
    with open(path, 'r') as ifile:
        # Create the CSV reader
        reader = csv.reader(ifile, quotechar='"')
        for row in reader:

            # Wrangle data
            try:
                row = list(map(lambda i: i.strip(), row))
                row[1] = row[1].split(" ")
                row[3] = datetime.strptime(row[3], DATEFORMAT)

                if len(row) > 5:
                    row[4] = ", ".join(row[4:])
                    row = row[:5]

            except Exception as e:
                print("{}: {}".format(e, row))
                continue

            # Yield a commit data structure
            yield Commit(*row)


def create_graph(path):
    """
    Creates a graph from the data set
    """
    g = nx.Graph(name='Sklearn Commits')

    # Make first pass to add commits and parents
    for commit in parse_dataset(path):

        g.add_node(commit.commit, timestamp=commit.timestamp, type='commit')  # add other elements?
        g.add_node(commit.contributor, type='contributor')
        g.add_edge(commit.contributor, commit.commit, label='contributor')

        for parent in commit.parents:
            g.add_node(parent, type='commit')
            g.add_edge(parent, commit.commit, label='parent')

    # Make second pass to add time delta weights on parents
    def elapsed(G, edge):
        src = G.node[edge[0]]
        dst = G.node[edge[1]]

        if src['type'] == 'contributor' or dst['type'] == 'contributor':
            return None

        if 'timestamp' not in src or 'timestamp' not in dst:
            return 0.0

        return (dst['timestamp'] - src['timestamp']).total_seconds()

    elapsed = partial(elapsed, g)
    for edge in g.edges():
        g[edge[0]][edge[1]]['elapsed'] = elapsed(edge)

    return g


def write_graphml(g, outpath):
    """
    Converts data types then writes the graphml
    """

    def convert(data):
        """
        Converts a dictionary
        """
        for key in list(data.keys()):
            val = data[key]

            if isinstance(val, datetime):
                data[key] = val.strftime(ISO8601_DATETIME)

            if isinstance(val, type(None)):
                del data[key]

    # Convert node data types
    for node in g.nodes():
        convert(g.node[node])

    # Convert edge data types
    for edge in g.edges():
        convert(g[edge[0]][edge[1]])

    nx.write_graphml(g, outpath)


if __name__ == '__main__':

    g = create_graph(INPATH)
    write_graphml(g, GRAPHML)
    print(nx.info(g))
