import networkx as nx
import matplotlib.pyplot as plt


G = nx.karate_club_graph()
nx.write_adjlist(G, "graph.adjlist")

nx.draw(G)
plt.show()
