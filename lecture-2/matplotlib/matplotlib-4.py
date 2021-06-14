import networkx as nx
import matplotlib.pyplot as plt


# Importing graphs from a file
G = nx.read_graphml('../../dataset/graph-schema/graph.graphml')

# Draw with default node labels
nx.draw(G, with_labels=True)
plt.show()
