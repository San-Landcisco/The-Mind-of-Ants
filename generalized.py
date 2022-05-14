import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Individual:
    def __init__(self, state_vector):
        self.state_vector = state_vector

class Network:
    def __init__(self, graph, census, maps):
        self.graph = graph #underlying graph object of the network
        self.census = census #dictionary from nodes in graph to individuals
        self.maps = maps

    def state(self, node):
        return self.census[node].state_vector

    def print(self):
        for node in self.graph.nodes:
            print(self.state(node))

    def update(self):
        new_state = {}
        for node in self.graph.nodes:
            new_state[node] = np.zeros(len(self.state(node)))
            for source in self.graph.predecessors(node):
                new_state[node] += self.maps[(source,node)].dot(self.state(source))
        for node in self.graph.nodes:
            self.census[node].state_vector = new_state[node]

    def plot_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size = 250)
        nx.draw_networkx_edges(self.graph, pos, edgelist=self.graph.edges)
        plt.show()
        plt.close()

G = nx.DiGraph()
G.add_edges_from([(1,2),(1,3),(3,1)])

A = Individual(np.array([1,0]))
B = Individual(np.array([0,1]))
C = Individual(np.array([1,1]))

AtB = np.array([[1,0],[0,1]])
AtC = np.array([[1,-1],[-1,1]])
CtA = np.array([[-1,0],[0,-1]])

test = Network(G, {1:A,2:B,3:C}, {(1,2):AtB,(1,3):AtC,(3,1):CtA})

if __name__ == '__main__':

    DEPTH = 10

    test.plot_graph()

    for iteration in range(DEPTH):
        test.print()
        test.update()
