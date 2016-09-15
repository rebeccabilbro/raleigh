import graph_tool.all as gt
from numpy import sqrt

g = gt.load_graph('data/tiny_keyphrases.graphml.gz')

def degree_filter(degree=0):
    def inner(vertex):
        return vertex.out_degree() > degree
    return inner

g = gt.GraphView(g, vfilt=degree_filter(3))


deg = g.degree_property_map("out")
deg.a = 4 * (sqrt(deg.a) * 0.5 + 0.4)

ebet = gt.betweenness(g)[1]
ebet.a /= ebet.a.max() / 10.

eorder = ebet.copy()
eorder.a *= -1
pos = gt.sfdp_layout(g)

# control = g.new_edge_property("vector<double>")
# for e in g.edges():
#     d = sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2)) / 5
#     control[e] = [0.3, d, 0.7, d]

gt.graph_draw(g,
    pos=pos, vertex_size=deg,
    # edge_color=ebet, eorder=eorder, edge_pen_width=ebet,
    output='images/tiny_keyphrases.png',
)
