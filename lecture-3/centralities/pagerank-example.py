import networkx as nx
import matplotlib.pyplot as plt
import pprint as pp


with open('graph-pagerank.txt') as f:
    lines = f.readlines()

edgeList = [line.strip().split() for line in lines]

G = nx.DiGraph()
G.add_edges_from(edgeList)

ppr1 = nx.pagerank(G)

pp.pprint(ppr1)

pos = nx.planar_layout(G)
nx.draw(G, pos, with_labels=True, node_color="#f86e00")
plt.show()
