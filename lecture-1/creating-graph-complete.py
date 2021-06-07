import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_nodes_from([('1', {'label': 'Person', 'name': 'John Doe', 'age': 40}),
                  ('2', {'label': 'Person', 'name': 'Anna Doe', 'age': 25}),
                  ('3', {'label': 'Person', 'name': 'Harry Doe', 'age': 34})])

G.add_nodes_from([('4', {'label': 'CreditCard', 'provider': 'Visa', 'compromised': False}),
                  ('5', {'label': 'CreditCard', 'provider': 'Maestro', 'compromised': False}),
                  ('6', {'label': 'CreditCard', 'provider': 'Diners', 'compromised': True})])

G.add_edges_from([('1', '4'), ('2', '5'), ('3', '6')], type='OWNS')

G.add_node('7', label='Store', name='Walmart')
G.add_node('8', label='Store', name='Walgreens')
G.add_node('9', label='Store', name='H&M')

G.add_node('10', label='Category', name='Grocery store')
G.add_node('11', label='Category', name='Pharmacy')
G.add_node('12', label='Category', name='Clothing store')

G.add_node('13', label='Pos', compromised=False)
G.add_node('14', label='Pos', compromised=False)
G.add_node('15', label='Pos', compromised=False)

G.add_edges_from([('7', '10'), ('8', '11'), ('9', '12')],
                 type='IS_PART_OF_CATEGORY')

G.add_edges_from([('7', '13'), ('8', '14'), ('9', '15')],
                 type='HAS_POS_DEVICE')

G.add_node('16', label='Transaction', fraudReported=False)
G.add_node('17', label='Transaction', fraudReported=False)
G.add_node('18', label='Transaction', fraudReported=False)
G.add_node('19', label='Transaction', fraudReported=False)
G.add_node('20', label='Transaction', fraudReported=False)
G.add_node('21', label='Transaction', fraudReported=False)

G.add_edges_from([('4', '16'), ('4', '17'), ('4', '18'),
                  ('5', '19'), ('5', '20'), ('6', '21')],
                 type='HAS_TRANSACTION')

G.add_edges_from([('16', '13'), ('17', '14'), ('18', '15'),
                  ('19', '13'), ('20', '14'), ('21', '15')],
                 type='TRANSACTION_AT')

G.add_node('22', label='SocialMedia', username='john_doe', platform='Facebook', followers=2000)
G.add_node('23', label='SocialMedia', username='john_doe', platform='Twitter',  followers=20200)
G.add_node('24', label='SocialMedia', username='john_doe', platform='Instagram',  followers=29000)
G.add_node('25', label='SocialMedia', username='john_doe', platform='LinkedIn',  followers=900)
G.add_node('26', label='SocialMedia', username='anna_doe', platform='YouTube',  followers=33000)
G.add_node('27', label='SocialMedia', username='anna_doe', platform='Twitter',  followers=31000)
G.add_node('28', label='SocialMedia', username='harry_doe', platform='Facebook',  followers=2000)

G.add_edges_from([('1', '22'), ('1', '23'), ('1', '24'), ('1', '25'),
                  ('2', '26'), ('2', '27'), ('3', '28')],
                 type='HAS_ACCOUNT')

print(G.nodes)
print(G.edges)

pos = nx.spring_layout(G)

nx.draw(G, pos)
node_labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels=node_labels)

plt.show()
