import opinion_graph as og
from model import Model
from tqdm import tqdm
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, graph, model: Model, steps):
        self.steps = steps
        self.graph = graph
        self.model = model

    def run(self, display_nth=0):
        og.plot_opinions(self.graph, f"Opinion distribution at step 0")
        extn, extp, avg = [], [], []
        for i in tqdm(range(1, self.steps+1)):
            self.graph = self.model.step(self.graph)

            # calculate some metrics
            nextn, nextp, total = 0, 0, 0
            for j in self.graph.nodes():
                op = self.graph.nodes[j]['opinion']
                if op <= -0.95:
                    nextn += 1
                elif op >= 0.95:
                    nextp += 1
                total += op
            total /= self.graph.number_of_nodes()
            extn.append(nextn)
            extp.append(nextp)
            avg.append(total)

            if display_nth != 0 and i % display_nth == 0:
                # print(f"person 0 has opinion {self.graph.nodes[0]['opinion']}")
                og.plot_opinions(self.graph, f"Opinion distribution at step {i}")

        plt.plot(extn)
        plt.plot(extp)
        plt.show()
        plt.plot(avg)
        plt.show()
        self.show_metrics()

    def show_metrics(self):
        og.plot_opinions(self.graph, f"Opinion distribution")
