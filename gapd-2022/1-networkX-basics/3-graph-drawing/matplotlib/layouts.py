import networkx as nx
import matplotlib.pyplot as plt

G = nx.dodecahedral_graph()

# spring layout is default - position nodes using Fruchterman-Reingold force-directed algorithm.
# Draw the graph G with Matplotlib.
# nx.draw(G)
# plt.show()

# shell layout - position nodes in concentric circles.
# nx.draw(G, pos=nx.shell_layout(G))
# plt.show()

# spiral layout - position nodes in a spiral layout.
nx.draw(G, pos=nx.spiral_layout(G))
plt.show()
