import networkx as nx
import numpy as np
import pandas as pd
import random
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from stellargraph import StellarGraph
from stellargraph.data import BiasedRandomWalk
from stellargraph.data import EdgeSplitter
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

        walks = rw.run(
            nodes=list(G.nodes()),
            length=32,
            n=10,
            p=0.5,
            q=2.0,
        )
        print("Number of random walks: {}".format(len(walks)))

        str_walks = [[str(n) for n in walk] for walk in walks]

        model = Word2Vec(str_walks, size=128, window=5,
                         min_count=0, sg=1, workers=2, iter=1)

        model.wv.save_word2vec_format(embeddings_file_path)

    return load_embedding(embeddings_file_path)


def split_data(G):
    edge_splitter_test = EdgeSplitter(G)

    graph_test, X_test, y_test = edge_splitter_test.train_test_split(
        p=0.1, method="global"
    )
    edge_splitter_train = EdgeSplitter(graph_test, G)
    _, X_train, y_train = edge_splitter_train.train_test_split(
        p=0.1, method="global"
    )
    return X_train, y_train, X_test, y_test


def operator_avg(u, v):
    u = np.array(u)
    v = np.array(v)
    return (u + v) / 2.0


def link_examples_to_features(X_train, embeddings, binary_operator):
    return [
        binary_operator(embeddings[src], embeddings[dst])
        for src, dst in X_train
    ]


def train_classifier(X_train, y_train, embeddings, binary_operator):
    clf = LogisticRegressionCV(
        Cs=10, cv=10, scoring="roc_auc", max_iter=3000)
    X_features = link_examples_to_features(
        X_train, embeddings, binary_operator
    )
    clf.fit(X_features, y_train)
    return clf


def evaluate_roc_auc(clf, X_features, y):
    predicted = clf.predict_proba(X_features)
    positive_column = list(clf.classes_).index(1)
    return roc_auc_score(y, predicted[:, positive_column])


def test_classifier(X_test, y_test, embeddings, binary_operator, clf):
    X_features = link_examples_to_features(
        X_test, embeddings, binary_operator
    )
    score = evaluate_roc_auc(clf, X_features, y_test)
    print(f"ROC AUC score: {score}")


def main():
    G_nx = load_graph('git_edges.csv', 'git_nodes.csv')
    G = sample_graph(G_nx, 10000, 0)
    embeddings = calculate_embeddings(False, G, 'embeddings.txt')
    X_train, y_train, X_test, y_test = split_data(G)
    clf = train_classifier(X_train, y_train, embeddings, operator_avg)
    test_classifier(X_test, y_test, embeddings, operator_avg, clf)


if __name__ == "__main__":
    main()
