import networkx as nx
import matplotlib.pyplot as plt


# Importing graphs from a file
G = nx.read_graphml('../../dataset/graph-schema/graph.graphml')

# Draw with custom node labels
pos=nx.spring_layout(G)
nx.draw(G, pos)
node_labels = nx.get_node_attributes(G,'label')
nx.draw_networkx_labels(G, pos, labels = node_labels)
plt.show()
