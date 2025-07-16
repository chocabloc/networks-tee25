import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def create(num_nodes, directed=False, graph_params=(4, 0.2), alpha=0.3, eta=0.2, delta=0.3, trust=None, seed=None):
    # for reproducability
    if seed is not None:
        np.random.seed(seed)

    # social networks look like watts-strogatz graphs
    k, p = graph_params
    G = nx.connected_watts_strogatz_graph(num_nodes, k, p)

    # assign node attributes
    # we should explore assigning more of these randomly
    for node in G.nodes():
        G.nodes[node]['opinion'] = np.random.uniform(-1, 1)
        G.nodes[node]['delta'] = delta
        G.nodes[node]['alpha'] = alpha
        G.nodes[node]['eta'] = eta

    # assign edge weights ("trust")
    if trust is None:
        for u, v in G.edges():
            G[u][v]['trust'] = np.random.uniform(0.1, 0.8)
    else:
        for u, v in G.edges():
            G[u][v]['trust'] = trust

    # TODO: actually explore directed graphs?
    if directed:
        G = G.to_directed()

    return G

def plot_opinions(G, title):
    opinions = [G.nodes[i]['opinion'] for i in G.nodes()]
    plt.hist(opinions, bins=100, range=(-1, 1), color='skyblue')
    plt.title(title)
    plt.xlabel("Opinion")
    plt.ylabel("Frequency")
    plt.show()
