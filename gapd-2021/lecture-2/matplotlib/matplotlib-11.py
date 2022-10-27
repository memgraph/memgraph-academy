import networkx as nx
import matplotlib.pyplot as plt


K33 = nx.complete_bipartite_graph(3,3)

positions = {0:[-1,1], 1:[0,1], 2:[1,1], 3:[-1,-1], 4:[0,-1], 5:[1,-1]}
ax = plt.figure().gca()
ax.set_axis_off()
options = {'node_size' : 100, 'node_color' : 'k'}
nx.draw_networkx(K33, positions, with_labels=False, **options)
plt.show()