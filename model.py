from abc import ABC, abstractmethod
import numpy as np
import copy

class Model(ABC):
    @abstractmethod
    def step(self, g):
        pass

class BabyModel(Model):
    def __init__(self, delta):
        self.delta = delta

    def opinew(self, G):
        self.new_opinions = {}
        for i in G.nodes():
            o_i = G.nodes[i]['opinion']
            alpha_i = G.nodes[i]['alpha']
            total_delta = 0
            for j in G.neighbors(i):
                o_j = G.nodes[j]['opinion']
                trust_ij = G[i][j]['trust']
                delta_ij = abs(o_i - o_j)
                feedback = o_j if delta_ij <= self.delta else -o_j
                total_delta += trust_ij * (feedback - o_i)
            self.new_opinions[i] = o_i + alpha_i * total_delta

    def update_opinions(self, G):
        for i in G.nodes():
            G.nodes[i]['opinion'] = np.clip(self.new_opinions[i], -1, 1)

    def update_trust(self, G):
        H= G.copy()  
        for i in G.nodes():
            eta_i = G.nodes[i]['eta']
            o_i = G.nodes[i]['opinion']
            for j in G.neighbors(i):
                o_j = G.nodes[j]['opinion']
                sim = 1 - abs(o_i - o_j)
                trust_old = G[i][j]['trust']
                trust_new = trust_old + eta_i * (sim - trust_old)
                H[i][j]['trust'] = np.clip(trust_new, 0, 1)
        return H

    def step(self, g):
        self.opinew(g)
        g =  self.update_trust(g)
        self.update_opinions(g)
        return g

class NewModel(Model):
    def update_opinions(self, g, newg):
        # loop through all nodes
        for i in g.nodes():
            alpha_i, delta_i = g.nodes[i]['alpha'], g.nodes[i]['delta']
            o_i, op_shift, total_scale = g.nodes[i]['opinion'], 0, 0

            # sum up contributions from all neighbours to calculate shift in opinion
            for j in g.neighbors(i):
                o_j, trust = g.nodes[j]['opinion'], g[i][j]['trust']
                op_diff = o_j - o_i
                feedback = 1 if abs(op_diff) <= delta_i else 0
                scale = alpha_i*trust*feedback
                op_shift += scale*op_diff
                total_scale += 1
            op_shift /= total_scale

            # finally, update the opinion
            newg.nodes[i]['opinion'] = np.clip(o_i + op_shift, -1, 1)  

    def update_trust(self, g, newg):
        # loop through all nodes
        for i in g.nodes():
            o_i, eta_i = g.nodes[i]['opinion'], g.nodes[i]['eta']

            # update trust in all neighbours
            for j in g.neighbors(i):
                o_j, trust = g.nodes[j]['opinion'], g[i][j]['trust']
                similarity = 1 - abs(o_j - o_i)
                change = eta_i*(similarity - trust)
                newg[i][j]['trust'] = np.clip(trust + change, 0, 1)

    def step(self, g):
        newg = copy.deepcopy(g)
        self.update_opinions(g, newg)
        self.update_trust(g, newg)
        return newg
