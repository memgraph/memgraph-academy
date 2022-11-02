from cProfile import label
import matplotlib.pyplot as plt
import networkx as nx

gml_graph = nx.read_gml("networkX-basics/graph-creation/data/power.gml", label="id")

options = {"node_color": "black", "node_size": 50, "linewidths": 0, "width": 0.1}

pos = nx.spring_layout(gml_graph, seed=1969)  # Seed for reproducible layout
nx.draw(gml_graph, pos, **options)
plt.show()
