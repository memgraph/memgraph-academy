import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.pyplot import figure
from networkx.algorithms.components import weakly_connected_components, strongly_connected_components


with open('graph-components.txt') as f:
    lines = f.readlines()

edgeList = [line.strip().split() for line in lines]

G = nx.DiGraph()
G.add_edges_from(edgeList)

figure(figsize=(14, 6))
ax = plt.subplot(1, 3, 1)
ax.title.set_text("Input graph ")
nx.draw_networkx(G)

weak_components = weakly_connected_components(G)
strong_components = strongly_connected_components(G)

W = [G.subgraph(c).copy() for c in weakly_connected_components(G)]
S = [G.subgraph(c).copy() for c in strongly_connected_components(G)]

weak_component = max(W, key=len)
strong_component = max(S, key=len)

ax = plt.subplot(1, 3, 2)
ax.title.set_text("Weakly Connected Components ")
pos = nx.spring_layout(weak_component)
nx.draw_networkx(weak_component)

ax = plt.subplot(1, 3, 3)
ax.title.set_text("Strongly Connected Components ")
pos = nx.spring_layout(strong_component)
nx.draw_networkx(strong_component)

plt.show()
