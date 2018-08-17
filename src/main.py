from game.snake import Snake, Apple, render
from nn.NN import NN
import numpy as np
from nn.genetics import Generation

if __name__ == '__main__':

    generation = Generation()

    while True:
        generation.update()
        render(generation.snakes, generation.apples)