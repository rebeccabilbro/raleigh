#!/usr/bin/env python3

#############################################################################
# Imports
#############################################################################

import os
import time
import pickle
import networkx as nx


#############################################################################
# Fixtures
#############################################################################

DATA       = os.path.join(os.path.dirname(__file__), 'data')
PICKLE     = os.path.join(DATA, 'keyphrases.pickle')
GRAPHML    = os.path.join(DATA, 'keyphrases.graphml')


def timeit(func):
    """
    Standard timing decorator
    """

    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        return result, time.time() - start

    return wrapper


#############################################################################
# Specialized write-graphml function
#############################################################################

@timeit
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

    with open(PICKLE, 'rb') as f:
        g = pickle.load(f)

    _, seconds = write_graphml(g, GRAPHML)
    print("Wrote GraphML in {:0.2f} seconds".format(seconds))
