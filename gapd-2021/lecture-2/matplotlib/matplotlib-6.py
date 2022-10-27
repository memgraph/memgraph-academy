import networkx as nx
import matplotlib.pyplot as plt


# Importing graphs from a file
G = nx.read_graphml('../../dataset/graph-schema/graph.graphml')

# Draw with custom edge labels
pos=nx.spring_layout(G)
print(G.edges(data=True))
nx.draw(G, pos)
edge_labels = nx.get_edge_attributes(G,'type')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
plt.show()
