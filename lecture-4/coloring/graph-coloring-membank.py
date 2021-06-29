import networkx as nx
import matplotlib.pyplot as plt
import random


def sample_graph(G, number_of_samples, seed):
    random.seed(seed)
    H = G.copy()
    samples = random.sample(list(G.nodes()), number_of_samples)
    for n in G:
        if n not in samples:
            H.remove_node(n)
    return H


colors = [
    "blue", "gray", "pink",
    "red", "orange", "purple",
    "brown", "yellow", "green"]

G = nx.read_gexf('../../dataset/graph-small/graph.gexf')

# Select defined number of random nodes from a graph
# because the complete one is too big to visualize properly
G = sample_graph(G, 100, 0)
d = nx.coloring.equitable_color(G, num_colors=9)

node_colors = []
for i in d.keys():
    node_colors.append(colors[d[i]])

nx.draw(G, node_color=node_colors, with_labels=True)
plt.show()
