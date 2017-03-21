import pygame
import random
from Snake import *

pygame.init()

dsp_width = 800
dsp_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

sna_w, sna_h = 10, 10
speed = [10, 0]

screen = pygame.display.set_mode((dsp_width, dsp_height))
clock = pygame.time.Clock()

crashed = False
sna = Snake(20, 20, 20, 20)


rect = pygame.rect.Rect((400,300,sna_w,sna_h))

#rect_food = pygame.rect.Rect((100, 300, sna_w, sna_h))
rect_food = pygame.rect.Rect((600, 300, sna_w, sna_h))

pygame.draw.rect(screen, white, rect_food)
#pygame.draw.rect(screen, white, rect_food1)

snake_length = 0
pos_list = []
li = []

speed_list = []


while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = [-sna_w, 0]
            if event.key == pygame.K_RIGHT:
                speed = [sna_w, 0]
            if event.key == pygame.K_UP:
                speed = [0, -sna_h]
            if event.key == pygame.K_DOWN:
                speed = [0, sna_h]

    pos_list.append(rect.copy())
    rect.move_ip(speed)
    print(pos_list[-snake_length:])



    if rect.colliderect(rect_food):
        snake_length +=1

        x_r = random.randrange(0, 800,10)
        y_r = random.randrange(0, 600,10)
        rect_food = pygame.rect.Rect(x_r, y_r, sna_w+30, sna_h+30)

    screen.fill(black)

    pos_list_re = pos_list[-snake_length:]

    for re in pos_list_re:
        #_ = pos_list_re[-re:].copy()
        pygame.draw.rect(screen, white, re)
    #for rects in li:
       # pygame.draw.rect(screen, white, rects)


    pygame.draw.rect(screen, white, rect)
    pygame.draw.rect(screen, white, rect_food)

    pygame.display.update()
    clock.tick(10)

