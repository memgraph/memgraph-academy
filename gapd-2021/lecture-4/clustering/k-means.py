import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict
from matplotlib import cm
from sklearn import cluster


def draw_communities(G, clustering_labels, pos):

    # Convert clustering_labels to a dict where key=cluster_id, value=list of nodes in cluster
    cluster_dict = defaultdict(list)
    for node_id, cluster_id in enumerate(clustering_labels):
        cluster_dict[cluster_id].append(node_id)

    # Normalize number of clusters for choosing a color
    norm = colors.Normalize(vmin=0, vmax=len(cluster_dict.keys()))

    for club, members in cluster_dict.items():
        nx.draw_networkx_nodes(G, pos,
                               nodelist=members,
                               node_color=cm.jet(norm(club)),
                               node_size=100,
                               alpha=0.8)

    plt.title("Results of clustering")
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()


def graph_to_edge_matrix(G):
    # Initialize edge matrix with zeros
    edge_matrix = np.zeros((len(G), len(G)), dtype=int)

    # Loop to set 0 or 1 (diagonal elements are set to 1)
    for node in G:
        for neighbor in G.neighbors(node):
            edge_matrix[int(node)][int(neighbor)] = 1
        edge_matrix[int(node)][int(node)] = 1

    return edge_matrix


G = nx.karate_club_graph()
number_of_clusters = 2

# Convert a networkx graph into an edge matrix
edge_matrix = graph_to_edge_matrix(G)

# K-means clustering - this one is not very suited for our dataset
model = cluster.KMeans(n_clusters=number_of_clusters, n_init=1000)
model.fit(edge_matrix)
clustering_labels = list(model.labels_)

pos = nx.spring_layout(G)
# Draw the nodes to a plot with assigned colors for each individual cluster
draw_communities(G, clustering_labels, pos)
