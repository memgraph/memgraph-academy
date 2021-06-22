import networkx as nx
import matplotlib.pyplot as plt


def draw_network(G, layout, colors, position, draw_labels, title):

    ax = plt.subplot(position)
    ax.title.set_text(title)

    nx.draw(G,
            pos=layout,
            node_size=50,
            node_color=colors,
            edge_color='g')

    if draw_labels:
        node_labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos=layout, labels=node_labels)

G = nx.read_gexf('../../dataset/graph-small/graph.gexf')

centrality = nx.degree_centrality(G)
colors = list(centrality.values())

draw_network(G, nx.spring_layout(G), colors, 221,
             draw_labels=False, title='Degree centrality')

centrality = nx.closeness_centrality(G)
colors = list(centrality.values())

draw_network(G, nx.spring_layout(G), colors, 222,
             draw_labels=False,  title='Closeness centrality')

centrality = nx.betweenness_centrality(G)
colors = list(centrality.values())

draw_network(G, nx.spring_layout(G), colors, 223,
             draw_labels=False,  title='Betweenness centrality')

centrality = nx.katz_centrality(G)
colors = list(centrality.values())

draw_network(G, nx.spring_layout(G), colors, 224,
             draw_labels=False,  title='Katz centrality')

plt.show()
