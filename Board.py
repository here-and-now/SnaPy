import pygame
import random
import time
import numpy as np
from constants import *

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

snake_length = 0
pos_list = []
dsp_width = 800
dsp_height = 600
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
sna_w, sna_h = 10, 10
speed = [10, 0]


pygame.init()
screen = pygame.display.set_mode((dsp_width, dsp_height))
clock = pygame.time.Clock()
start_time = time.time()

x_r = random.randrange(200, 600, 10)
y_r = random.randrange(150, 450, 10)

head = pygame.rect.Rect((400, 300, sna_w, sna_h))
food = pygame.rect.Rect(x_r, y_r, sna_w + 30, sna_h + 30)
wall = pygame.rect.Rect((0, 0, dsp_width, dsp_height))

training_observation = []
action_dummy = []


crashed = False
#while not crashed:
for _ in range(100000):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    #
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #
    #             if speed[0] < 0:
    #                 speed = [0, sna_w]
    #             elif speed[0] > 0:
    #                 speed = [0, -sna_w]
    #
    #             elif speed[1] < 0:
    #                 speed = [-sna_w, 0]
    #             elif speed[1] > 0:
    #                 speed = [sna_w, 0]
    #
    #         if event.key == pygame.K_RIGHT:
    #
    #             if speed[0] < 0:
    #                 speed = [0, -sna_w]
    #             elif speed[0] > 0:
    #                 speed = [0, sna_w]
    #
    #             elif speed[1] < 0:
    #                 speed = [sna_w, 0]
    #             elif speed[1] > 0:
    #                 speed = [-sna_w, 0]

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         speed = [-sna_w, 0]
        #     if event.key == pygame.K_RIGHT:
        #         speed = [sna_w, 0]
        #     if event.key == pygame.K_UP:
        #         speed = [0, -sna_h]
        #     if event.key == pygame.K_DOWN:
        #         speed = [0, sna_h]
    action = random.randrange(0,2)
    action_dummy = 0

    if action == 0:

        action_dummy = [0, 1]
        if speed[0] < 0:
            speed = [0, sna_w]
        elif speed[0] > 0:
            speed = [0, -sna_w]


        elif speed[1] < 0:
            speed = [-sna_w, 0]
        elif speed[1] > 0:
            speed = [sna_w, 0]

    elif action == 1: # rechts
        action_dummy = [1, 0]
        if speed[0] < 0:
            speed = [0, -sna_w]
        elif speed[0] > 0:
            speed = [0, sna_w]

        elif speed[1] < 0:
            speed = [sna_w, 0]
        elif speed[1] > 0:
            speed = [-sna_w, 0]

    if snake_length > 0:
        pos_list.append(head.copy())

    head.move_ip(speed)
    screen.fill(black)

    if head.colliderect(food):
        snake_length +=1

        x_r = random.randrange(200, 600, 10)
        y_r = random.randrange(150, 450, 10)
        food = pygame.rect.Rect(x_r, y_r, sna_w + 30, sna_h + 30)



    # if snake_length > 0:
    #     pos_list = pos_list[-snake_length:]
    #     for re in pos_list:
    #         pygame.draw.rect(screen, white, re)

    #if head.collidelist(pos_list) != -1 or not wall.contains(head):
    if not wall.contains(head):
        snake_length = 0
        head = pygame.rect.Rect((400, 300, sna_w, sna_h))

        x_r = random.randrange(200, 600, 10)
        y_r = random.randrange(150, 450, 10)
        food = pygame.rect.Rect(x_r, y_r, sna_w + 30, sna_h + 30)

        pygame.draw.rect(screen, white, head)
        fitness = 0
        speed = [10, 0]

    pygame.draw.rect(screen, white, head)
    pygame.draw.rect(screen, green, food)
    pygame.draw.rect(screen, red, wall, 5)
    pygame.display.update()

    elapsed_time = time.time() - start_time
    fitness = snake_length + 0.1 * elapsed_time
    training_observation.append([action_dummy[0],action_dummy[1], head.center[0], head.center[1], food.center[0],food.center[1], fitness])



    clock.tick(30000)
#X = np.array(training_observation).reshape(-1,5,1)

#print(X)
#training_observation = np.array(training_observation)
#print(training_observation)
#np.save('training_data', training_observation)




def neural_network_model(input_size):
    network = input_data(shape=[None, input_size], name='input')

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation='relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation='relu')
    network = dropout(network, 0.8)

    # network = fully_connected(network, 256, activation='relu')
    # network = dropout(network, 0.8)
    #
    # network = fully_connected(network, 128, activation='relu')
    # network = dropout(network, 0.8)

    network = fully_connected(network, 2, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(network, tensorboard_dir='log')

    return model

def train_model(training_data, model=False):

    X = np.array([i[2:] for i in training_data]).reshape(-1, 5)
    print(X)
    # print(X.shape)
    # print('X',X)
    #print('y:t',training_data[0,5])
    y = np.array([i[:2] for i in training_data]).reshape(-1, 2)


      #a = np.asarray
    print('len X: y',len(X), len(y))
    print('shape X: y', X.shape, y.shape)
    #print('y',y.shape)

    #print(len(X[:5]))
    if not model:
        model = neural_network_model(input_size=5)

    model.fit({'input':X}, {'targets':y}, n_epoch=5, snapshot_step=10, show_metric=True,
              run_id='snapy')

    return model

model = train_model(training_observation)
