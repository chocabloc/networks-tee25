#Baby model: random graph/watts strogatz
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#Problems:
num_nodes = 100
p = 0.5          
k = 4      
d = 0.4          
steps = 100
alpha = 0.3
eta = 0.2
def initialize_graph(seed=None):
    if seed is not None:
        np.random.seed(seed)  #  for reproducibility
    G = nx.connected_watts_strogatz_graph(num_nodes, k, p)
    for node in G.nodes():
        G.nodes[node]['opinion'] = np.random.uniform(-1, 1)
        G.nodes[node]['agreeableness'] = alpha  # use variable
        G.nodes[node]['loyalty'] = eta #np.random.uniform(0.1, 0.9)
    for u, v in G.edges():
        G[u][v]['trust'] = np.random.uniform(0.1, 0.8)
    return G

def opinew(G):
    new_opinions = {}
    for i in G.nodes():
        o_i = G.nodes[i]['opinion']
        alpha_i = G.nodes[i]['agreeableness']
        total_delta = 0
        for j in G.neighbors(i):
            o_j = G.nodes[j]['opinion']
            trust_ij = G[i][j]['trust']
            delta_ij = abs(o_i - o_j)
            feedback = o_j if delta_ij <= d else -o_j
            total_delta += trust_ij * (feedback - o_i)
        new_opinions[i] = o_i + alpha_i * total_delta
    return new_opinions

def update_opinions(G, new_opinions):
    for i in G.nodes():
        G.nodes[i]['opinion'] = np.clip(new_opinions[i], -1, 1)

def update_trust(G):
    H= G.copy()  
    for i in G.nodes():
        eta_i = G.nodes[i]['loyalty']
        o_i = G.nodes[i]['opinion']
        for j in G.neighbors(i):
            o_j = G.nodes[j]['opinion']
            sim = 1 - abs(o_i - o_j)
            trust_old = G[i][j]['trust']
            trust_new = trust_old + eta_i * (sim - trust_old)
            H[i][j]['trust'] = np.clip(trust_new, 0, 1)
    G = H

def plot_opinions(G, step):
    opinions = [G.nodes[i]['opinion'] for i in G.nodes()]
    plt.hist(opinions, bins=40, range=(-1, 1), color='skyblue')
    plt.title(f"Opinion Distribution at Step {step}. Standard deviation = {np.std(opinions[1:98]):.2f}")
    plt.xlabel("Opinion")
    plt.ylabel("Frequency")
    plt.show()
G = initialize_graph(seed=42)
plot_opinions(G, step=0)  
for t in range(steps):
    new_opinions = opinew(G)
    update_trust(G)
    update_opinions(G, new_opinions)
    if  t%10==0 or t==steps - 1:
        plot_opinions(G, step=t)
