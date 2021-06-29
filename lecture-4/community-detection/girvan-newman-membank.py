import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman


def remove_unnecessary_data(G):
    H = G.copy()
    for node in H.nodes(data=True):
        if node[1]['label'] == 'SocialMedia':
            G.remove_node(node[0])
    G.remove_nodes_from(list(nx.isolates(G)))
    return G


def get_color(i, r_off=1, g_off=1, b_off=1):
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 4) % n) / (n-1)
    g = low + span * (((i + g_off) * 8) % n) / (n-1)
    b = low + span * (((i + b_off) * 12) % n) / (n-1)
    return (r, g, b)


G = nx.read_gexf('../../dataset/graph-small/graph.gexf')

# Remove social media accounts and isolates from the dataset
G = remove_unnecessary_data(G)

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
