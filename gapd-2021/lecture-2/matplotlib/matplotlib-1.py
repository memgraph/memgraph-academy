import networkx as nx
import matplotlib.pyplot as plt


G = nx.dodecahedral_graph()

nx.draw(G)
plt.show()

# This will draw a graph with the same layout (spring layout is the default one)
nx.draw(G, pos=nx.spring_layout(G))
plt.show()
