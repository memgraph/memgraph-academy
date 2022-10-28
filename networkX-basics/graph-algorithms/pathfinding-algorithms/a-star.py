import networkx as nx

G = nx.path_graph(5)
print(nx.astar_path(G, 0, 4))
[0, 1, 2, 3, 4]
G = nx.grid_graph(dim=[3, 3])  # nodes are two-tuples (x,y)
nx.set_edge_attributes(G, {e: e[1][0] * 2 for e in G.edges()}, "cost")


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


print(nx.astar_path(G, (0, 0), (2, 2), heuristic=dist, weight="cost"))
