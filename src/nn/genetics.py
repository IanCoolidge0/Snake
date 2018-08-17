import numpy as np
from game.snake import Snake, Apple
from nn.NN import NN, from_flat

GEN_SIZE = 50

class Generation(object):

    snakes = []
    NNs = []
    apples = []

    def __init__(self):
        for _ in range(GEN_SIZE):
            self.snakes.append(Snake())
            self.NNs.append(NN())
            self.apples.append(Apple())

    def update(self):
        for i in range(GEN_SIZE):
            if not self.snakes[i].is_dead:
                move = self.NNs[i].result(self.snakes[i].get_input(self.apples[i]))
                self.snakes[i].update(move)
                #print(i)    

def crossover(c1, c2, p1, p2):    
    return np.concatenate([c1[:p1], c2[p1:p2], c1[p2:]])

def mutate(c, mut_count=2):
    for _ in range(mut_count):
        index = np.random.randint(len(c))
        val = np.random.uniform(-1.0, 1.0)
        c[index] = val

        