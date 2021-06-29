import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.algorithms.components import weakly_connected_components


colorlist = ['r', 'g', 'b', 'y', 'c', 'm', 'k']

g = nx.read_gexf('../../dataset/graph-small/graph.gexf')

wcc_subgraphs = [g.subgraph(wcc) for wcc in weakly_connected_components(g)]

# There are 7 weakly connected components and we are plotting the three biggest ones
# that represent customers of a specific store. They all have transaction at that POS device.
for i, subgraph in enumerate(wcc_subgraphs):
    randIndex = random.randint(0, len(colorlist) - 1)
    if(len(subgraph.nodes()) > 10):
        plt.subplot(2, 2, i+1)
        nx.draw(subgraph, node_color=colorlist[randIndex])

plt.show()
