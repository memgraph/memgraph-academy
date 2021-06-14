import networkx as nx
import matplotlib.pyplot as plt

G = nx.star_graph(10)

nx.draw(G)
plt.show()
