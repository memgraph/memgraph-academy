import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_adjlist("graph.adjlist")

nx.draw(G)
plt.show()