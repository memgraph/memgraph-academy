import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Importing graphs from a file
G = nx.read_graphml("gapd-2022/1-networkX-basics/3-graph-drawing/data/graph.graphml")

# Defining the node colors
colors = np.linspace(0, 1, len(G.nodes))

pos = nx.circular_layout(G)
nx.draw(
    G, pos, node_size=1000, node_color=colors
)  # draws directed graph, nx.draw(G, arrows=False) for removing arrows

# Draw node labels and change font size
node_labels = nx.get_node_attributes(G, "label")
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, "type")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


plt.show()
