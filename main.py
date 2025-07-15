import opinion_graph as og
from model import BabyModel, NewModel
from simulation import Simulation


# run 'Baby Model'
"""
graph = og.create(num_nodes=100, graph_params=(4, 0.5), alpha=0.3, eta=0.2, seed=42)
model = BabyModel(delta=0.4)
sim = Simulation(graph, model, steps=100)
sim.run()
"""

# run the new model
graph = og.create(num_nodes=1000, directed=True, graph_params=(4, 0.04), alpha=0.3, eta=0.2, delta=0.4, trust=0, seed=42)
model = NewModel()
sim = Simulation(graph, model, steps=1000)
sim.run(display_nth=0)
