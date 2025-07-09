import opinion_graph as og
from model import BabyModel
from simulation import Simulation

graph = og.create(num_nodes=100, directed=True)
model = BabyModel(delta=0.2)

sim = Simulation(graph, model, steps=100)
sim.run(display_nth=1)
