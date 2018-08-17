from game.snake import Snake, Apple, render

if __name__ == '__main__':

    snake = Snake()
    apple = Apple()
    while True:
        snake.update()
        render(snake, apple)