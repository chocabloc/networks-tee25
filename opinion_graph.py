import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def create(num_nodes, directed=False, k=8, p=0.1):
    G = nx.watts_strogatz_graph(num_nodes, k, p)
    for node in G.nodes():
        G.nodes[node]['opinion'] = np.random.uniform(-1, 1)
        G.nodes[node]['agreeableness'] = 0.5  # np.random.uniform(0.2, 1.0)
        G.nodes[node]['loyalty'] = 0.1  # np.random.uniform(0.1, 0.9)
    for u, v in G.edges():
        G[u][v]['trust'] = np.random.uniform(0.1, 0.8)
    if directed:
        G = G.to_directed()
    return G

def plot_opinions(G, title):
    opinions = [G.nodes[i]['opinion'] for i in G.nodes()]
    plt.hist(opinions, bins=40, range=(-1, 1), color='skyblue')
    plt.title(title)
    plt.xlabel("Opinion")
    plt.ylabel("Frequency")
    plt.show()
