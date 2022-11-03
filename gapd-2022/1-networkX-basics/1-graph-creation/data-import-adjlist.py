import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_adjlist("gapd-2022/1-networkX-basics/1-graph-creation/data/graph.adjlist")

nx.draw(G)
plt.show()
