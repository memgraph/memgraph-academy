import csv
import networkx as nx
import random


number_of_people = 1000
number_of_stores = 3
max_number_of_transactions = 50
max_number_of_social_account = 3


def write_nodes_csv(node_label):
    with open('graph-large/' + node_label + '.csv', mode='w') as file:
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
    nx.write_gexf(G, 'graph-large/' + file_name + '.gexf')


def write_graph_gml(file_name):
    nx.write_graphml(G, 'graph-large/' + file_name + '.graphml')


people_names_list = ['Krystle Blas', 'Jeri Tardy', 'Clarinda Sappington', 'Jonas Parkerson', 'Florance Yaeger',
                     'Carlton Casaus', 'Nathanial Bridgers', 'Ivana Stmartin', 'Alethea Shedrick', 'Mirian Scarbrough',
                     'Randal Blackshire', 'Jean Mathena', 'Wally Zamzow', 'Vern Proto', 'Rodney Yale', 'Shari Damelio',
                     'Davis Calbert', 'Ozie Rowan', 'Dot Brautigam', 'Ileen Brungardt']

credit_card_providers = ['Visa', 'Maestro', 'Diners']

stores_categories_dict = {'Walmart': 'Grocery store',
                          'Walgreens': 'Pharmacy',
                          'H&M': 'Clothing store'}
number_of_stores = len(stores_categories_dict)

social_media_accounts_list = ['Facebook',
                              'Twitter', 'LinkedIn', 'Instagram', 'YouTube']
number_of_social_media_accounts = len(social_media_accounts_list)

G = nx.DiGraph()

node_id = 0
for i in range(0, number_of_people):
    G.add_nodes_from(
        [(node_id, {'label': 'Person', 'name': random.choice(people_names_list), 'age': random.randint(21, 80)}),
         (node_id + number_of_people, {'label': 'CreditCard', 'provider': random.choice(credit_card_providers), 'compromised': False})])
    G.add_edge(node_id, node_id + number_of_people, type='OWNS')
    node_id = node_id + 1
node_id = node_id + number_of_people

for key, value in stores_categories_dict.items():
    G.add_nodes_from(
        [(node_id, {'label': 'Store', 'name': key}),
         (node_id + number_of_stores, {'label': 'Category', 'name': value}),
         (node_id + number_of_stores * 2, {'label': 'Pos', 'compromised': False})])
    G.add_edge(node_id, node_id + number_of_stores, type='IS_PART_OF_CATEGORY')
    G.add_edge(node_id, node_id + number_of_stores * 2, type='HAS_POS_DEVICE')
    node_id = node_id + 1

node_id = node_id + number_of_stores * 2
credit_card_id = number_of_people
pos_id_min = number_of_people * 2 + number_of_stores * 2
pos_id_max = pos_id_min + number_of_stores
for i in range(0, number_of_people):
    for i in range(0, random.randint(0, max_number_of_transactions)):
        G.add_node(node_id, label='Transaction', fraudReported=False)
        G.add_edge(credit_card_id, node_id, type='HAS_TRANSACTION')
        G.add_edge(random.randint(pos_id_min, pos_id_max),
                   node_id, type='HAS_TRANSACTION')
        node_id = node_id + 1
    credit_card_id = credit_card_id + 1

for i in range(0, number_of_people):
    for social_media_account in random.sample(social_media_accounts_list, random.randint(0, number_of_social_media_accounts)):
        G.add_node(node_id, label='SocialMedia', username=random.choice(people_names_list).lower(),
                   platform=social_media_account, followers=random.randint(0, 10000))
        G.add_edge(i, node_id, type='HAS_ACCOUNT')
        node_id = node_id + 1

write_nodes_csv('Person')
write_nodes_csv('CreditCard')
write_nodes_csv('Store')
write_nodes_csv('Category')
write_nodes_csv('Pos')
write_nodes_csv('Transaction')
write_nodes_csv('SocialMedia')

write_graph_gexf('graph')

write_graph_gml('graph')
