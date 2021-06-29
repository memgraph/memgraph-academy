import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman


def get_color(i, r_off=1, g_off=1, b_off=1):
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 4) % n) / (n-1)
    g = low + span * (((i + g_off) * 8) % n) / (n-1)
    b = low + span * (((i + b_off) * 12) % n) / (n-1)
    return (r, g, b)


G = nx.karate_club_graph()

communities = girvan_newman(G)

node_groups = []
for community in next(communities):
    node_groups.append(list(community))

node_colors = []
for ng in range(len(node_groups)):
    for node in G:
        if node in node_groups[ng]:
            node_colors.append(get_color(ng))

nx.draw(G, node_color=node_colors)
plt.show()
