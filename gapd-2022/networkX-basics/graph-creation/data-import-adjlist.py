import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_adjlist("networkX-basics/graph-creation/data/graph.adjlist")

nx.draw(G)
plt.show()
