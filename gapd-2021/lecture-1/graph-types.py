import networkx as nx
import matplotlib.pyplot as plt

G = nx.complete_graph(5, nx.Graph())

plt.subplot(121)
nx.draw(G)

G = nx.complete_graph(5, nx.MultiDiGraph())

plt.subplot(122)
nx.draw(G, connectionstyle='arc3, rad = 0.1')

plt.show()
