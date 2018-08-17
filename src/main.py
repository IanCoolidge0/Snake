from game.snake import Snake, Apple, render
from nn.NN import NN
import numpy as np

if __name__ == '__main__':

    snake = Snake()
    apple = Apple()

    nn = NN()

    while True:
        snake.update()
        render(snake, apple)