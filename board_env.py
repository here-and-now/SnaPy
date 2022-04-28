import pygame
import random
import math
import sys
import time
import numpy as np
import gym
from collections import deque
# import tflearn
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression


window_width, window_height = 800,800


black, white, green, red = (0,0,0), (255,255,255), (0,255,0), (255,0,0)

SNAKE_LEN_GOAL=30

class SnapyEnv(gym.Env):

    # def __init__(self,rend=False,rendrate=50):FG
    def __init__(self, **kwargs):
        super(SnapyEnv, self).__init__()
        # inits
        self.window_width = 1000
        self.window_height = 1000
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
                                            shape=(5+SNAKE_LEN_GOAL,), dtype=np.int32)

        # start fresh
        self.reset()


    def reset(self):
        # previous actions and positions list/deque 
        self.previous_positions = []
        self.previous_actions = deque(maxlen=SNAKE_LEN_GOAL)

        # clean slate
        self.head = pygame.rect.Rect(self.window_width/2, self.window_height/2, self.pixel, self.pixel)

        self.done = False
        self.score = 0
        self.reward = 0
        self.snake_length = 2
        self.place_food()
        
        print(self.food_reward)
       
        # append nonsense data for nonexistent prev actions
        for _ in range(SNAKE_LEN_GOAL):
            self.previous_actions.append(-1)

        # construct observation space
        observation = [self.head.centerx, self.head.centery, self.food.centerx, self.food.centery, self.snake_length] + list(self.previous_actions)
        observation = np.array(observation)
        return observation 
   
 
    def step(self,action):
        self.previous_actions.append(action) 
        self.previous_positions.append(self.head.center)

        if action == 0:
            self.head.centerx = self.head.centerx - self.pixel
        if action == 1:
            self.head.centerx = self.head.centerx + self.pixel
        if action == 2:
            self.head.centery = self.head.centery - self.pixel
        if action == 3:
            self.head.centery = self.head.centery + self.pixel


        self.check_death()
        self.check_food() 

        self.info = {}
        self.reward = self.score
        
        observation = [self.head.centerx, self.head.centery, self.food.centerx, self.food.centery, self.snake_length] + list(self.previous_actions)
        observation = np.array(observation) 
        
        return observation, self.reward, self.done, self.info 
        

    def check_death(self):
        if self.head.centerx > self.window_width or self.head.centerx < 0 or self.head.centery > self.window_height or self.head.centery < 0:
            self.done = True
            self.score += self.wall_reward
        elif self.snake_length > 1 and self.head.center in self.previous_positions[-self.snake_length:]:
            self.done = True
            self.score += self.ouroboros_reward
    
    def check_food(self):
        if self.head.center == self.food.center:
            self.snake_length += 1
            self.place_food()
            self.score += self.food_reward
    
    def euclidean_dist_to_food(self):
        return np.linalg.norm(np.array(self.snake_head.center) - np.array(self.food.center))


    def render(self):
        if not self.rend:
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((self.window_width, self.window_height))
            self.rend = True
            
        self.screen.fill(black)
        pygame.draw.rect(self.screen, red, self.head)
        pygame.draw.rect(self.screen, green, self.food)

            
        body = pygame.rect.Rect(0,0, self.pixel, self.pixel )
        for (prev_pos) in self.previous_positions[-self.snake_length:]:
            body.center = prev_pos
            pygame.draw.rect(self.screen, white, body)

        pygame.display.update()
        self.clock.tick(self.rendrate)
        
   
    def place_food(self):
        x = random.randrange(0, self.window_width, self.pixel)
        y = random.randrange(0, self.window_height, self.pixel)
        self.food = pygame.rect.Rect(x,y,self.pixel, self.pixel)

        if self.food.center in self.previous_positions[-self.snake_length:]:
            self.place_food()

# b = SnapyEnv()
# b.step()


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

# old step function, working
# def step(self,action=0):
        # while True:
            # action = random.randrange(0,4) # left, right,up, down
            # self.previous_positions.append(self.head.center)
            # self.previous_actions.append(action)

            # manual = False
            # # manual = True
            # if manual:
                # pygame.event.clear()
                # waiting = True
                # while waiting:
                    # events = [pygame.event.wait()]
                    # for event in events:
                        # if event.type == pygame.KEYUP:
                            # waiting = False
                            # if event.key == pygame.K_LEFT:
                                # self.head.centerx = self.head.centerx - self.pixel
                            # elif event.key == pygame.K_RIGHT:
                                # self.head.centerx = self.head.centerx + self.pixel
                            # elif event.key == pygame.K_UP:
                                # self.head.centery = self.head.centery - self.pixel
                            # elif event.key == pygame.K_DOWN:
                                # self.head.centery = self.head.centery + self.pixel
            # else:        
                # if action == 0:
                    # self.head.centerx = self.head.centerx - self.pixel
                # if action == 1:
                    # self.head.centerx = self.head.centerx + self.pixel
                # if action == 2:
                    # self.head.centery = self.head.centery - self.pixel
                # if action == 3:
                    # self.head.centery = self.head.centery + self.pixel

            # self.check_death()
            # self.check_food()
            
            # if self.done:
                # self.reward = - 10
                # self.reset()
            # else:
                # self.reward = self.score
     
            # self.render()
            # self.info = {}
        
            # observation = [self.head.centerx, self.head.centery, self.food.centerx, self.food.centery, self.snake_length] + list(self.previous_actions)

            # observation = np.array(observation) 
            # # print(self.observation.shape)
            # # print(self.observation)
            # return observation, self.reward, self.done, self.info 
            



