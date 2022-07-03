import random
import math
import sys
import time
import numpy as np
import gym
from collections import deque
import torch
import pygame
window_width, window_height = 800,800
black, white, green, red = (0,0,0), (255,255,255), (0,255,0), (255,0,0)


SNAKE_LEN_GOAL=30

class SnapyEnv(gym.Env):
    def __init__(self, **kwargs):
        super(SnapyEnv, self).__init__()

        # inits
        self.window_width = 900
        self.window_height = 900
        self.pixel = 100
        self.rend = False
        self.rendrate = 3

        # standard rewards
        self.food_reward = 0
        self.step_reward = 0
        self.ouroboros_reward = 0
        self.wall_reward = 0
        
        # pass reward kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # gym spaces
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=-1000, high=1000,
                                            shape=(5+SNAKE_LEN_GOAL,), dtype=np.float32)
        # start fresh
        self.reset()


    def reset(self):
        # previous actions and positions list/deque 
        self.previous_positions = []
        self.previous_actions = deque(maxlen=SNAKE_LEN_GOAL)
        self.previous_pos = deque(maxlen=SNAKE_LEN_GOAL)

        # clean slate
        self.head = (self.window_width/2, self.window_height/2)

        self.done = False
        self.score = 0
        self.reward = 0
        self.prev_reward = 0
        self.snake_length = 2

        self.place_food()
       
        # append nonsense data for nonexistent prev actions
        for _ in range(SNAKE_LEN_GOAL):
            self.previous_actions.append(-1)
            self.previous_pos.append((-1,-1))
        self.previous_pos[-1] = self.head
        self.previous_pos[-2] = self.head

         
        prevs = list(sum(list(self.previous_pos), ()))
        # construct observation space
        observation = [self.head[0], self.head[1],
                       # self.food[0], self.food[1],
                       self.food[0] - self.head[0], self.food[1] - self.head[1],
                       self.snake_length] + list(self.previous_actions)
                       # self.snake_length] + prevs

        observation = np.array(observation, dtype=np.float32)
        return observation 
   
    # def flatten(self):
    def step(self,action):
        self.previous_actions.append(action) 
        self.previous_positions.append(self.head)

        self.head = list(self.head)
        if action == 0:
            self.head[0] = self.head[0] - self.pixel
        if action == 1:
            self.head[0] = self.head[0] + self.pixel
        if action == 2:
            self.head[1] = self.head[1] - self.pixel
        if action == 3:
            self.head[1] = self.head[1] + self.pixel
        self.head = tuple(self.head)

        self.previous_pos.append(self.head)

        self.score += self.check_death()
        self.score += self.check_food()
        
        self.reward = self.reward + self.score
        # self.reward = self.reward - self.prev_reward
        # self.prev_reward = self.reward

        # if self.done:
            # self.reward = -10


        self.info = {}
        prevs = list(sum(list(self.previous_pos), ()))

        observation = [self.head[0], self.head[1],
                       # self.food[0], self.food[1],
                       self.food[0] - self.head[0], self.food[1] - self.head[1],
                       self.snake_length] + list(self.previous_actions)
                       # self.snake_length] + prevs
        
        observation = np.array(observation, dtype=np.float32)
        return observation, self.reward, self.done, self.info 
        

    def check_death(self):
        if self.head[0] >= self.window_width  or self.head[0] <= 0 or \
           self.head[1] >= self.window_height or self.head[1] <= 0:
            self.done = True
            return self.wall_reward
        elif self.head in self.previous_positions[-self.snake_length:]:
            self.done = True
            return self.ouroboros_reward
        else:
            return self.step_reward
            
    
    def check_food(self):
        if self.head == self.food:
            self.snake_length += 1
            self.place_food()
            return self.food_reward
        else:
            # return -self.euclidean_dist_to_food()/100
            return 0
    
    def euclidean_dist_to_food(self):
        return np.linalg.norm(np.array(self.head) - np.array(self.food))


    def render(self):
        if not self.rend:
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))
            self.rend = True
        
         
        head = pygame.rect.Rect(0, 0, self.pixel, self.pixel)
        food = pygame.rect.Rect(0, 0, self.pixel, self.pixel)
        head.center = self.head
        food.center = self.food
    

        self.screen.fill(black)
        pygame.draw.rect(self.screen, red, head)
        pygame.draw.rect(self.screen, green, food)

            
        body = pygame.rect.Rect(0,0, self.pixel, self.pixel )
        for (prev_pos) in self.previous_positions[-self.snake_length:]:
            body.center = prev_pos
            pygame.draw.rect(self.screen, white, body)

        pygame.display.update()
        self.clock.tick(self.rendrate)
        
   
    def place_food(self):
        x = random.randrange(0+self.pixel/2, self.window_width-self.pixel/2, self.pixel)
        y = random.randrange(0+self.pixel/2, self.window_height-self.pixel/2, self.pixel)
        # self.food = pygame.rect.Rect(x,y,self.pixel, self.pixel)
        self.food = (x,y)
        if self.food in self.previous_positions[-self.snake_length:]:
            self.place_food()


