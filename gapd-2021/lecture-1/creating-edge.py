import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge('1', '2', type='CONNECTED_TO')

print(G.edges)

pos = nx.spring_layout(G)

nx.draw(G, pos)

edge_labels = nx.get_edge_attributes(G, 'type')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
