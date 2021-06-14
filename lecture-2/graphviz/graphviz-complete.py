import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


G = nx.read_gexf('../../dataset/graph-large/graph.gexf')

A = to_agraph(G)
print(A)
A.layout('dot')
A.draw('output/graphviz-complete.png')
