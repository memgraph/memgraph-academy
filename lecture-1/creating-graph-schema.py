import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_nodes_from([('1', {'label': 'Person', 'name': 'John Doe', 'age': 40})])

G.add_nodes_from([('2', {'label': 'CreditCard', 'name': 'Visa', 'compromised': False})])

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

G.add_node('22', label='SocialMedia', username='john_doe', platform='Facebook', followers=2000)

G.add_edges_from([('1', '22')], type='HAS_ACCOUNT')

print(G.nodes)
print(G.edges)

pos = nx.spring_layout(G)

nx.draw(G, pos)
node_labels = nx.get_node_attributes(G,'label')
nx.draw_networkx_labels(G, pos, labels = node_labels)

edge_labels = nx.get_edge_attributes(G,'type')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)

plt.show()
