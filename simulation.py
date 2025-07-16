import opinion_graph as og
from model import Model
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import networkx as nx
import numpy as np

class Simulation:
    def __init__(self, graph, model: Model, steps):
        self.steps = steps
        self.graph = graph
        self.model = model

    def run(self, display_nth=0):
        self.history = []

        og.plot_opinions(self.graph, f"Opinion distribution at step 0")
        extn, extp, pavg, navg, avg = [], [], [], [], []
        for i in tqdm(range(1, self.steps+1)):
            self.history.append(np.array([self.graph.nodes[n]['opinion'] for n in self.graph.nodes()]))
            self.graph = self.model.step(self.graph)

            # calculate some metrics
            nextn, nextp, total, totalp, totaln, pn, nn = 0, 0, 0, 0, 0, 0, 0
            for j in self.graph.nodes():
                op = self.graph.nodes[j]['opinion']
                if op <= -0.75:
                    nextn += 1
                elif op >= 0.75:
                    nextp += 1
                total += op
                if op < 0:
                    totaln += op
                    nn += 1
                else:
                    pn += 1
                    totalp += op
            total /= self.graph.number_of_nodes()
            #totalp /= pn
            #totaln /= nn
            extn.append(nextn)
            extp.append(nextp)
            avg.append(total)
            pavg.append(totalp)
            navg.append(totaln)

            # display distribution if we need to
            if display_nth != 0 and i % display_nth == 0:
                # print(f"person 0 has opinion {self.graph.nodes[0]['opinion']}")
                og.plot_opinions(self.graph, f"Opinion distribution at step {i}")

        plt.plot(extp)
        plt.plot(extn)
        plt.show()
        plt.plot(pavg)
        plt.plot(navg)
        plt.show()
        plt.plot(avg)
        plt.show()
        self.show_metrics()
        #self.export_vid()

    def export_vid(self):
        pos = nx.spring_layout(self.graph)
        normed = (self.history[0] + 1)/2

        fig, ax = plt.subplots(figsize=(8, 6))
        edges = nx.draw_networkx_edges(self.graph, pos, edge_color='gray', alpha=0.3)
        nodes = nx.draw_networkx_nodes(
            self.graph, pos,
            node_color=normed,
            cmap='coolwarm',
            node_size=30,
            ax=ax
        )

        sm = plt.cm.ScalarMappable(cmap='coolwarm', norm=plt.Normalize(vmin=-1, vmax=1))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('Opinion')
        
        ax.set_axis_off()
        ax.set_title("Opinion Heatmap")
        
        def update(i):
            h_i = self.history[i]
            normed = (h_i+1)/2
            nodes.set_array(normed)
            return [nodes]
            
        a = anim.FuncAnimation(fig, update, frames=len(self.history), interval=50, blit=True, repeat_delay=1000)
        plt.show()


    def show_metrics(self):
        og.plot_opinions(self.graph, f"Opinion distribution")
