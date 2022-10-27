import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# Importing graphs from a file
G = nx.read_gexf('../../dataset/graph-schema/graph.gexf')

nx.draw(G,
        node_size=30,
        node_color='C1')

plt.show()

# Defining the node colors
colors = np.linspace(0, 1, len(G.nodes))

layout = nx.spiral_layout(G)

nx.draw(G,
        node_size=30,
        node_color=colors,
        pos=layout,
        edge_color='g')

plt.show()
