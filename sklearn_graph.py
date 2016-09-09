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
import datetime
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

#############################################################################
# Fixtures
#############################################################################
INPATH     = 'sklearncommits_mini.txt' # full set was slow so clipped last 2yrs
IMGPATH    = 'sklearngraph.png'
GRAPHML    = 'sklearngraph.graphml'
DATEFORMAT = '%a %b %d %I:%M:%S %Y %z'

g = nx.Graph(name='Sklearn Commits')

ifile   = open(os.path.join('data', INPATH), 'r')
commits  = csv.reader(ifile)

for commit in commits:
    commit_hash = commit[0]     # Uniquely identifies a commit
    parent_hashes = commit[1]
    contributor = commit[2]
    try: 
        commit_timestamp = datetime.datetime.strptime(commit[3], DATEFORMAT).date()
    except:
        pass

    g.add_node(commit_hash, timestamp=commit_timestamp)  # add other elements?
    g.add_node(contributor)
    g.add_edge(contributor, commit_hash, label='contributor')

    for parent in parent_hashes:
        g.add_node(parent, timestamp=commit_timestamp)
        delta = g.node[parent]['timestamp']-g.node[commit_hash]['timestamp']
        g.add_edge(parent, commit_hash, label='parent', weight=delta.total_seconds())

print("Nodes of graph: ")
print(g.nodes())
print("Edges of graph: ")
print(g.edges())

nx.draw(g)
plt.show()
# plt.savefig(os.path.join('images', IMGPATH))
nx.write_graphml(g)
