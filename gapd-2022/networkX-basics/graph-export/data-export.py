import networkx as nx
import matplotlib.pyplot as plt


G = nx.petersen_graph()
nx.write_adjlist(G, "networkX-basics/graph-export/data/graph.adjlist")
nx.write_gml(G, "networkX-basics/graph-export/data/graph.gml")
nx.write_graphml(G, "networkX-basics/graph-export/data/graph.graphml")

nx.draw(G, pos=nx.shell_layout(G), node_color="#FB6E00")
plt.show()
