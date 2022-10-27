import networkx as nx
import matplotlib.pyplot as plt
import pprint as pp


G = nx.read_edgelist('./graph-flow.txt', nodetype=str,
                     data=(('capacity', int),), create_using=nx.DiGraph())

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color="#f86e00")

flow = nx.maximum_flow(G, _s="s", _t="t")
flow_value = nx.maximum_flow_value(G, _s="s", _t="t")

pp.pprint(flow)
print("Maximum flow value is: " + str(flow_value))

plt.show()
