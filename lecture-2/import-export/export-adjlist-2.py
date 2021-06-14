import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_graphml('../../dataset/graph-schema/graph.graphml')

nx.write_gpickle(G, 'graph.gpickle')
G_imported = nx.read_gpickle('graph.gpickle')

nx.draw(G, with_labels=True)
plt.show()
