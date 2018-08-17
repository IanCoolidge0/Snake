#!/usr/bin/env python

import pygame
import sys
import time
import random
import numpy as np

from pygame.locals import *

FPS = 20
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE=10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (0,0,0)
        self.is_dead = False
    
    def reset(self):
        self.is_dead = False

    def turn_left(self):
        if self.direction == UP:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = UP

    def turn_right(self):
        if self.direction == UP:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = UP

    def update(self, move=-1):
        if move == -1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.point(UP)
                    elif event.key == K_DOWN:
                        self.point(DOWN)
                    elif event.key == K_LEFT:
                        self.point(LEFT)
                    elif event.key == K_RIGHT:
                        self.point(RIGHT)
        elif move == 0:
            pass
        elif move == 1:
            self.turn_left()
        elif move == 2:
            self.turn_right()

    def food_ray(self, apple):
        cur = self.positions[0]
        x, y = self.direction
        temp_pos = (((cur[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)

        while temp_pos != cur:
            xp, yp = temp_pos
            if xp < 0 or xp > 620 or yp < 0 or yp > 460:
                return 0
            if temp_pos == apple.position:
                return 1
            temp_pos = (((temp_pos[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (temp_pos[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
        
        return 0

    def food_distance(self, apple):
        x1, y1 = self.positions[0]
        x2, y2 = apple.position
        return abs(y2 - y1) + abs(x2 - x1)

    def facing_wall(self, pos):
        x, y = pos
        return x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT

    def get_input(self, apple):
        brain_input = np.ndarray((6,))
        
        cur = self.positions[0]
        x, y = self.direction
        new = cur[0]+x*GRIDSIZE, cur[1]+y*GRIDSIZE
        brain_input[0] = 1 - int((new in self.positions) or self.facing_wall(new))

        self.turn_left()
        x, y = self.direction
        new = cur[0]+x*GRIDSIZE, cur[1]+y*GRIDSIZE
        brain_input[1] = 1 - int((new in self.positions) or self.facing_wall(new))

        self.turn_right()
        self.turn_right()
        x, y = self.direction
        new = cur[0]+x*GRIDSIZE, cur[1]+y*GRIDSIZE
        brain_input[2] = 1 - int((new in self.positions) or self.facing_wall(new))

        brain_input[5] = self.food_ray(apple)
        self.turn_left()
        brain_input[3] = self.food_ray(apple)
        self.turn_left()
        brain_input[4] = self.food_ray(apple)
        self.turn_right()

        return brain_input

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.is_dead = True
        print("lost")

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = cur[0]+x*GRIDSIZE, cur[1]+y*GRIDSIZE
        x_new, y_new = new
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        elif x_new > SCREEN_WIDTH or x_new < 0 or y_new > SCREEN_HEIGHT or y_new < 0:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

class Apple(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surf):
        draw_box(surf, self.color, self.position)

def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 3
        apple.randomize()

def render(snakes, apples):

    surface.fill((255,255,255))
    for i in range(len(snakes)):
        if not snakes[i].is_dead:
            snakes[i].move()
            check_eat(snakes[i], apples[i])
            snakes[i].draw(surface)
            apples[i].draw(surface)

    font = pygame.font.Font(None, 36)
    text = font.render(str(snakes[0].length), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = 20
    surface.blit(text, textpos)
    screen.blit(surface, (0,0))

    pygame.display.flip()
    pygame.display.update()
    fpsClock.tick(FPS + snakes[0].length/3)