#!/usr/bin/env python3
# sklearn_graph.py

# Author:   Rebecca Bilbro <rebecca.bilbro@bytecubed.com>

#############################################################################
# Imports
#############################################################################
import os
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#############################################################################
# Fixtures
#############################################################################
INPATH   = 'sklearncommits_mini.txt'
OUTPATH  = 'sklearngraph.png'

g = nx.Graph(name="Sklearn Commits")

ifile   = open(os.path.join('data', INPATH), 'r')
commits  = csv.reader(ifile)
next(commits)
for commit in commits:
    commit_hash = commit[0]
    parent_hashes = commit[1]
    contributor = commit[2]
    commit_timestamp = commit[3]

    g.add_node(commit_hash, timestamp=commit_timestamp)
    g.add_node(contributor)
    g.add_edge(contributor, commit_hash, label='contributor')

    for parent in parent_hashes:
        g.add_node(parent)
        g.add_edge(parent, commit_hash, label='parent')


print("Nodes of graph: ")
print(g.nodes())
print("Edges of graph: ")
print(g.edges())

nx.draw(g)
# plt.savefig(os.path.join('images', OUTPATH))
plt.show()
