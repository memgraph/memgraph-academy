import networkx as nx
import matplotlib.pyplot as plt
import random


G = nx.read_gexf('../../dataset/graph-small/graph.gexf')

pagerank = nx.pagerank(G)

for node_id in G.nodes:
    G.nodes[node_id]['pagerank'] = round(pagerank[node_id], 5)

pos = nx.spring_layout(G)

nx.draw(G, pos)
node_labels = nx.get_node_attributes(G, 'pagerank')
nx.draw_networkx_labels(G, pos, labels=node_labels)

plt.show()
