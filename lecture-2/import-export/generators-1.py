import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()

nx.draw(G)
plt.show()
