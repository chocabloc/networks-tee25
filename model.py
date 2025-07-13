from abc import ABC, abstractmethod
import numpy as np

class Model(ABC):
    @abstractmethod
    def step(self, g):
        pass

class BabyModel(Model):
    def __init__(self, delta):
        self.delta = delta

   def opinew(G)->list:
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

    def update_opinions(G):
        for i in G.nodes():
            G.nodes[i]['opinion'] = np.clip(r[i], -1, 1)


    def update_trust(G):
        for i in G.nodes():
            eta_i = G.nodes[i]['loyalty']
            o_i = G.nodes[i]['opinion']
            for j in G.neighbors(i):
                o_j = G.nodes[j]['opinion']
                sim = 1 - abs(o_i - o_j)
                trust_old = G[i][j]['trust']
                trust_new = trust_old + eta_i * (sim - trust_old)
                G[i][j]['trust'] = np.clip(trust_new, 0, 1)


     def step(self, g):
        r= self.opinew(G)
        self.update_trust(G)
        self.update_opinions(G)
