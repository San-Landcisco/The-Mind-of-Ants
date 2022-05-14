import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
import math

PI = 3.14159

def rotation(angle):
    return np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])

class Ant:
    def __init__(self, heading = None):
        if heading == None:
            heading = random.uniform(0,2*PI)
        self.compass = np.array([math.cos(heading),math.sin(heading)])
        self.heading = heading

    def rebalance(self):
        self.compass = np.array([math.cos(self.heading),math.sin(self.heading)])

class Colony:
    lethargy = 30

    def __init__(self, members, friends):
        self.members = members #nodes of type ant
        self.friends = friends #directed edges

    def deliberate(self):
        resolution = {}

        self.members[5].heading += .1 % (2*PI)
        self.members[5].rebalance()

        for pair in self.friends:
            #disagreement = math.acos(pair[1].compass.dot(pair[0].compass))
            disagreement = pair[1].heading - pair[0].heading
            resolution[pair] = disagreement

        for pair in self.friends:
            #test = np.cross(pair[1].compass,pair[0].compass)

            if np.sign(resolution[pair]) <= 0:
                #pair[1].compass = rotation(-resolution[pair]/self.lethargy).dot(pair[1].compass)
                pair[1].heading = (pair[1].heading + (resolution[pair]%PI)/self.lethargy)%(2*PI)
                pair[1].rebalance()
            else:
                #pair[1].compass = rotation(resolution[pair]/self.lethargy).dot(pair[1].compass)
                pair[1].heading = (pair[1].heading - (resolution[pair]%PI)/self.lethargy)%(2*PI)
                pair[1].rebalance()

    def census(self):
        census_data = []

        for ant in self.members:
            census_data.append(ant.compass)

        return(np.array(census_data))

    def plot(self, label):
        data = self.census()

        origin = np.array([[0]*len(self.members),[0]*len(self.members)])

        image = plt.quiver(*origin, data[:,0], data[:,1], color = ['b','b','b','b','b','r'], scale=3)

        plt.xlim(-2,2)
        plt.ylim(-2,2)
        plt.axis('off')
        plt.savefig('AntArgument'+str(label))
        plt.close()

    def plot_network(self, label):
        G = nx.DiGraph()
        G.add_edges_from(self.friends)
#john = Ant()
#amy = Ant()
#cecil = Ant()
#ants = np.array([john,amy,cecil])

'''
ants1 = []

for k in range(5):
    ants1.append(Ant())

ants2 = []

for k in range(5):
    ants2.append(Ant())

antsrel1 = [(a,b) for a in ants1 for b in ants1]
antsrel2 = [(a,b) for a in ants2 for b in ants2]

antsrel = antsrel1 + antsrel2
antsrel.append((ants1[0],ants2[0]))
antsrel.append((ants2[0],ants1[0]))
ants = np.array(ants1 + ants2)
'''

ants = []
for k in range(5):
    ants.append(Ant())
antsrel = [(a,b) for a in ants for b in ants]

Leonard = Ant()
coolfella = [(Leonard, a) for a in ants]
antsrel = antsrel + coolfella

ants = np.array(ants + [Leonard])

antGang = Colony(ants, antsrel)

for step in range(150):
    antGang.plot(step)
    antGang.deliberate()
