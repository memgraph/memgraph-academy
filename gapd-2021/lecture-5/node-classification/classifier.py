import networkx as nx
import pandas as pd
import random
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score
from stellargraph import StellarGraph
from stellargraph.data import BiasedRandomWalk
from tqdm import tqdm


# Create a NetworkX graph from files
def load_graph(edges_file_path, nodes_file_path):
    edges = pd.read_csv(edges_file_path, sep=',')
    G = nx.from_pandas_edgelist(edges, 'id_1', 'id_2')

    nodes = pd.read_csv(nodes_file_path, sep=',')

    nx.set_node_attributes(G, pd.Series(
        nodes.developer_type, index=nodes.id).to_dict(), 'developer_type')
    nx.set_node_attributes(G, pd.Series(
        nodes.id, index=nodes.id).to_dict(), 'id')

    return G


# Select defined number of random nodes from a graph
def sample_graph(G, number_of_samples, seed):
    random.seed(seed)
    H = G.copy()
    samples = random.sample(list(G.nodes()), number_of_samples)
    for n in tqdm(G):
        if n not in samples:
            H.remove_node(n)

    H = StellarGraph.from_networkx(H)
    return H


# Load node embeddings from a file into a dictionary
def load_embedding(file_path):
    embedding_dict = {}
    first_line = True
    with open(file_path) as f:
        for line in f:
            if first_line:
                first_line = False
                continue
            vector = [float(i) for i in line.strip().split()]
            embedding_dict[int(vector[0])] = vector[1:]
        f.close()
    return embedding_dict


def calculate_embeddings(recalculate_embeddings, G, embeddings_file_path):
    if recalculate_embeddings == True:
        rw = BiasedRandomWalk(G)

        walks = rw.run(nodes=list(G.nodes()), length=32, n=10, p=0.5, q=2.0)
        print("Number of random walks: {}".format(len(walks)))

        str_walks = [[str(n) for n in walk] for walk in walks]

        model = Word2Vec(str_walks, size=128, window=5,
                         min_count=0, sg=1, workers=2, iter=1)
        model.wv.save_word2vec_format(embeddings_file_path)
    return load_embedding(embeddings_file_path)


def split_data(G_nx, embeddings):
    X = []
    y = []
    for x in embeddings.keys():
        X.append(embeddings[x])
        y.append(G_nx.nodes[x]['developer_type'])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test


def train_classifier(X_train, y_train):
    clf = LogisticRegressionCV(
        Cs=10, cv=10, scoring="accuracy", verbose=False, max_iter=3000
    )
    clf.fit(X_train, y_train)
    return clf


def test_classifier(X_test, y_test, clf):
    y_pred = clf.predict(X_test)

    print(f"Accuracy classification score: {accuracy_score(y_test, y_pred)}")


def main():
    G_nx = load_graph('git_edges.csv', 'git_nodes.csv')
    G = sample_graph(G_nx, 10000, 0)
    embeddings = calculate_embeddings(False, G, 'embeddings.txt')
    X_train, X_test, y_train, y_test = split_data(G_nx, embeddings)
    clf = train_classifier(X_train, y_train)
    test_classifier(X_test, y_test, clf)


if __name__ == "__main__":
    main()
