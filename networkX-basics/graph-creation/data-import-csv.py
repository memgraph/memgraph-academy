import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


use_pandas = True
g = nx.Graph()


if use_pandas:
    df = pd.read_csv("networkX-basics/graph-creation/data/graph.csv")
    G = nx.from_pandas_edgelist(df, create_using=g)
else:
    Data = open("networkX-basics/graph-creation/data/graph.csv", "r")
    next(Data, None)
    G = nx.parse_edgelist(Data, delimiter=",", create_using=g, nodetype=int)

nx.draw(G)
plt.show()
