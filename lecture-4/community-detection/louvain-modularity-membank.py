import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
# pip install python-louvain
from community import community_louvain


def remove_unnecessary_data(G):
    H = G.copy()
    for node in H.nodes(data=True):
        if node[1]['label'] == 'SocialMedia':
            G.remove_node(node[0])
    G.remove_nodes_from(list(nx.isolates(G)))
    return G


G = nx.read_gexf('../../dataset/graph-small/graph.gexf')
G = G.to_undirected()

# Remove social media accounts and isolates from the dataset
G = remove_unnecessary_data(G)

communities = community_louvain.best_partition(G)

pos = nx.spring_layout(G)

cmap = cm.get_cmap('viridis', max(communities.values()) + 1)
nx.draw_networkx_nodes(G, pos, communities.keys(),
                       cmap=cmap, node_color=list(communities.values()))
nx.draw_networkx_edges(G, pos, alpha=0.6)

plt.show()
