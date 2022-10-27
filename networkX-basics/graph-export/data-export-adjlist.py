import networkx as nx
import matplotlib.pyplot as plt


G = nx.petersen_graph()
nx.write_adjlist(G, "networkX-basics/graph-export/data/graph.adjlist")

nx.draw(G)
plt.show()
