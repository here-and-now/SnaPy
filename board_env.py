import pygame
import random
import math
import sys
import time
import numpy as np
import gym

# import tflearn
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression


window_width, window_height = 800,800


black, white, green, red = (0,0,0), (255,255,255), (0,255,0), (255,0,0)

class SnapyEnv(gym.Env):

    def __init__(self,env_config={}):
        self.window_width = 800
        self.window_height = 800
        self.pixel = 10
        self.init_render()
        self.reset()

    def init_render(self):

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def reset(self):
        self.done = False
        self.head = pygame.rect.Rect(self.window_width/2, self.window_height/2, self.pixel, self.pixel)
        self.place_food()
        self.score = 0
        prev_button_direction = 1
        button_direction = 2
        

        self.observation = {}        
        
        return self.observation
    
    def step(self):
        while True:
            action = random.randrange(0,4) # left, right, up, down
            
            if action == 0:
                self.head.centerx = self.head.centerx - self.pixel

            if action == 1:
                self.head.centerx = self.head.centerx + self.pixel

            if action == 2:
                self.head.centery = self.head.centery + self.pixel

            if action == 3:
                self.head.centery = self.head.centery - self.pixel

            self.render() 
            # self.head.move_ip(self.speed)
            # self.food_contact()

    def place_food(self):
        x = random.randrange(0, self.window_width, self.pixel)
        y = random.randrange(0, self.window_height, self.pixel)

        self.food = pygame.rect.Rect(x,y,self.pixel, self.pixel)
    
        
    def render(self):
        
        self.screen.fill(black)
        pygame.draw.rect(self.screen, white, self.head)
        pygame.draw.rect(self.screen, green, self.food)
        # pygame.draw.rect(self.screen, self.red, self.wall, 5)
        pygame.display.update()
        self.clock.tick(25)

        
b = SnapyEnv()
b.step()


# class Board():

    # def __init__(self):


    # def food_contact(self):
        # if self.head.colliderect(self.food):
            # self.snake_length += 1
            # self.food = pygame.rect.Rect(
                # (self.random_position()[0], self.random_position()[1], self.sna_w + 30, self.sna_h + 30))

    # def wall_contact(self):
        # if not self.wall.contains(self.head):
            # self.__init__()
            # return True
        # else:
            # return False

    # def euclidean_dist_to_food(self):
        # return math.sqrt(((self.head.center[0]-self.food[0])**2)
                         # +(self.head.center[1]-self.food[1])**2)

    # def pixeldata(self):
        # print(pygame.surfarray.array2d(self.screen))

    # def get_fitness(self):
        # elapsed_time = time.time() - self.start_time
        # return self.snake_length + 0.1 * elapsed_time



# action_memory = [x[1] for x in game_memory]
# game_memory = [x[0] for x in game_memory]


# game_memory = np.array(game_memory).reshape(-1, 6)
# action_memory = np.array(action_memory).reshape(-1, 1)
# print(game_memory.shape, action_memory.shape)

