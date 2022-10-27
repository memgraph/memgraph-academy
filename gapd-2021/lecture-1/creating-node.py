import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node('1', label='Person', name='John Doe', age=40)

print(G.nodes)

pos = nx.spring_layout(G)

nx.draw(G, pos)

node_labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels=node_labels)

plt.show()
