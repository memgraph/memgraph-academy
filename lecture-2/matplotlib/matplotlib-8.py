import networkx as nx
import matplotlib.pyplot as plt


K33 = nx.complete_bipartite_graph(3,3)

# Visualize the graph with the draw() method
nx.draw(K33)
plt.show()