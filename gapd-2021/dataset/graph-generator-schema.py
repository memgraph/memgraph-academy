import csv
import networkx as nx
import matplotlib.pyplot as plt
import random


def write_nodes_csv(node_label):
    with open('graph-schema/' + node_label + '.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for node_id in G.nodes:
            if(G.nodes[node_id]['label'] == node_label):
                attribute_list = []
                attribute_list.append(node_id)
                for _, value in G.nodes[node_id].items():
                    attribute_list.append(value)
                writer.writerow(attribute_list)


def write_graph_gexf(file_name):
    nx.write_gexf(G, 'graph-schema/' + file_name + '.gexf')


def write_graph_gml(file_name):
    nx.write_graphml(G, 'graph-schema/' + file_name + '.graphml')


G = nx.DiGraph()
G.add_nodes_from([('1', {'label': 'Person', 'name': 'John Doe', 'age': 40})])

G.add_nodes_from(
    [('2', {'label': 'CreditCard', 'name': 'Visa', 'compromised': False})])

G.add_edges_from([('1', '2')], type='OWNS')

G.add_node('3', label='Store', name='Walmart')

G.add_node('4', label='Category', name='Grocery store')

G.add_node('5', label='Pos', compromised=False)

G.add_edges_from([('3', '4')], type='IS_OF_CATEGORY')

G.add_edges_from([('3', '5')],
                 type='HAS_POS_DEVICE')

G.add_node('6', label='Transaction', fraudReported=False)

G.add_edges_from([('2', '6')], type='HAS_TRANSACTION')

G.add_edges_from([('6', '5')], type='TRANSACTION_AT')

G.add_node('22', label='SocialMedia', username='john_doe',
           platform='Facebook', followers=2000)

G.add_edges_from([('1', '22')], type='HAS_ACCOUNT')

print(G.nodes)
print(G.edges)

pos = nx.spring_layout(G)

nx.draw(G, pos)
node_labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels=node_labels)

edge_labels = nx.get_edge_attributes(G, 'type')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

write_nodes_csv('Person')
write_nodes_csv('CreditCard')
write_nodes_csv('Store')
write_nodes_csv('Category')
write_nodes_csv('Pos')
write_nodes_csv('Transaction')
write_nodes_csv('SocialMedia')

write_graph_gexf('graph')

write_graph_gml('graph')

plt.show()
