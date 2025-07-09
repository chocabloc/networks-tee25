import opinion_graph as og
from model import Model

class Simulation:
    def __init__(self, graph, model: Model, steps):
        self.steps = steps
        self.graph = graph
        self.model = model

    def run(self, display_nth=0):
        for i in range(1, self.steps+1):
            self.model.step(self.graph)
            if display_nth != 0 and i % display_nth == 0:
                print(f"person 0 has opinion {self.graph.nodes[0]['opinion']}")
                og.plot_opinions(self.graph, f"Opinion distribution at step {i}")
        self.show_metrics()

    def show_metrics(self):
        og.plot_opinions(self.graph, f"Opinion distribution")
