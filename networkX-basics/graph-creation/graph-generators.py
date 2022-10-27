from matplotlib import scale
import networkx as nx
import matplotlib.pyplot as plt


generated_graph = nx.les_miserables_graph()

# generated_graph = nx.star_graph(15)

pos = nx.spring_layout(generated_graph, scale=0.5)
nx.draw(generated_graph, pos)

print(nx.nodes(generated_graph))
edge_labels = nx.get_edge_attributes(generated_graph, "weight")

nx.draw_networkx_edge_labels(generated_graph, pos, edge_labels=edge_labels, font_size=6)
plt.show()
