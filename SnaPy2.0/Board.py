import pygame
import random
import math
import sys
import time
import numpy as np

# import tflearn
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression

game_memory = []
class Board():

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.dsp_width, self.dsp_height = 800, 600
        self.screen = pygame.display.set_mode((self.dsp_width, self.dsp_height))

        self.sna_w ,self.sna_h = 10, 10
        self.black, self.white, self.green, self.red = (0,0,0), (255,255,255), (0,255,0), (255,0,0)

        self.head = pygame.rect.Rect((400, 300, self.sna_w, self.sna_h))

        self.food = pygame.rect.Rect(
            (self.random_position()[0], self.random_position()[1], self.sna_w + 30, self.sna_h + 30))

        self.wall = pygame.rect.Rect((0, 0, self.dsp_width, self.dsp_height))

        self.snake_length = 0
        self.speed = [10, 0]
        self.start_time = time.time()

    def render(self):
        self.screen.fill(self.black)
        pygame.draw.rect(self.screen, self.white, self.head)
        pygame.draw.rect(self.screen, self.green, self.food)
        pygame.draw.rect(self.screen, self.red, self.wall, 5)
        pygame.display.update()
        self.clock.tick(25)


    def run(self, steps=0):
        counter = 0
        prev_observation = []
        observation = []


        while True:
            action = random.randrange(0,2)
            # links = 0, rechts = 1
            if action == 0:

                action_dummy = [0, 1]
                if self.speed[0] < 0:
                    self.speed = [0, self.sna_w]
                elif self.speed[0] > 0:
                    self.speed = [0, -self.sna_w]


                elif self.speed[1] < 0:
                    self.speed = [-self.sna_w, 0]
                elif self.speed[1] > 0:
                    self.speed = [self.sna_w, 0]
            elif action == 1:  # rechts
                action_dummy = [1, 0]
                if self.speed[0] < 0:
                    self.speed = [0, -self.sna_w]
                elif self.speed[0] > 0:
                    self.speed = [0, self.sna_w]

                elif self.speed[1] < 0:
                    self.speed = [self.sna_w, 0]
                elif self.speed[1] > 0:
                    self.speed = [-self.sna_w, 0]

            self.head.move_ip(self.speed)
            self.food_contact()
            if not self.wall_contact():
                observation = ([self.head.center[0],
                                self.head.center[1],
                                self.food.center[0],
                                self.food.center[1],
                                self.euclidean_dist_to_food(),
                                self.get_fitness()
                                ])
                if prev_observation:
                    game_memory.append([prev_observation[:6], action])
            prev_observation = observation
            print(len(game_memory))

            self.render()
            counter += 1
            if counter == steps:
                break


    def random_position(self):
        x = random.randrange(200, 600, 10)
        y = random.randrange(150, 450, 10)
        return x, y

    def food_contact(self):
        if self.head.colliderect(self.food):
            self.snake_length += 1
            self.food = pygame.rect.Rect(
                (self.random_position()[0], self.random_position()[1], self.sna_w + 30, self.sna_h + 30))

    def wall_contact(self):
        if not self.wall.contains(self.head):
            self.__init__()
            return True
        else:
            return False

    def euclidean_dist_to_food(self):
        return math.sqrt(((self.head.center[0]-self.food[0])**2)
                         +(self.head.center[1]-self.food[1])**2)

    def pixeldata(self):
        print(pygame.surfarray.array2d(self.screen))

    def get_fitness(self):
        elapsed_time = time.time() - self.start_time
        return self.snake_length + 0.1 * elapsed_time

b = Board()

b.run(5)

action_memory = [x[1] for x in game_memory]
game_memory = [x[0] for x in game_memory]


game_memory = np.array(game_memory).reshape(-1, 6)
action_memory = np.array(action_memory).reshape(-1, 1)
print(game_memory.shape, action_memory.shape)
