import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


def add_attribute_to_nodes(G, key, value, node_label):
    for node_id in G.nodes:
        if(G.nodes[node_id]['label'] == node_label):
            G.nodes[node_id][key] = value


G = nx.read_gexf('../../dataset/graph-schema/graph.gexf')

add_attribute_to_nodes(G, 'style', 'filled', 'Person')
add_attribute_to_nodes(G, 'fillcolor', 'red', 'Person')

add_attribute_to_nodes(G, 'style', 'filled', 'Store')
add_attribute_to_nodes(G, 'fillcolor', 'orange', 'Store')

G.edges['1', '2']['color'] = 'purple'
G.edges['1', '2']['arrowsize'] = 2.0
G.edges['1', '2']['penwidth'] = 2.0

G.graph['graph'] = {'rankdir': 'LR'}
G.graph['node'] = {'shape': 'circle'}
G.graph['edges'] = {'arrowsize': '4.0'}

A = to_agraph(G)
print(A)
A.layout('dot')
A.draw('output/graphviz-schema-2.png')
