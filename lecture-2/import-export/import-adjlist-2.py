import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


use_pandas = True
Graphtype = nx.Graph()

if use_pandas:
    df = pd.read_csv('graph.csv')
    G = nx.from_pandas_edgelist(df, create_using=Graphtype)
else:
    Data = open('graph.csv', "r")
    next(Data, None)
    G = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype,
                          nodetype=int)

nx.draw(G)
plt.show()
