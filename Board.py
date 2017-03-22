import pygame
import random
import time


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

head = pygame.rect.Rect((400, 300, sna_w, sna_h))
food = pygame.rect.Rect((600, 300, sna_w, sna_h))
wall = pygame.rect.Rect((0, 0, dsp_width, dsp_height))


#pygame.draw.rect(screen, red, wall)
#pygame.draw.rect(screen, white, food)


snake_length = 0
pos_list = []
print(speed[0])
crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:

                if speed[0] < 0:
                    speed = [0, sna_w]
                elif speed[0] > 0:
                    speed = [0, -sna_w]

                elif speed[1] < 0:
                    speed = [-sna_w, 0]
                elif speed[1] > 0:
                    speed = [sna_w, 0]

            if event.key == pygame.K_RIGHT:

                if speed[0] < 0:
                    speed = [0, -sna_w]
                elif speed[0] > 0:
                    speed = [0, sna_w]

                elif speed[1] < 0:
                    speed = [sna_w, 0]
                elif speed[1] > 0:
                    speed = [-sna_w, 0]

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         speed = [-sna_w, 0]
        #     if event.key == pygame.K_RIGHT:
        #         speed = [sna_w, 0]
        #     if event.key == pygame.K_UP:
        #         speed = [0, -sna_h]
        #     if event.key == pygame.K_DOWN:
        #         speed = [0, sna_h]

    if snake_length > 0:
        pos_list.append(head.copy())
    head.move_ip(speed)


    if head.colliderect(food):
        snake_length +=1

        x_r = random.randrange(0, dsp_width-10, 10)
        y_r = random.randrange(0, dsp_height-10, 10)
        food = pygame.rect.Rect(x_r, y_r, sna_w + 30, sna_h + 30)

    screen.fill(black)

    if snake_length > 0:
        pos_list = pos_list[-snake_length:]
        for re in pos_list:
            pygame.draw.rect(screen, white, re)

    if head.collidelist(pos_list) != -1 or not wall.contains(head):
        snake_length = 0
        head = pygame.rect.Rect((400, 300, sna_w, sna_h))
        pygame.draw.rect(screen, white, head)
        fitness = 0
        speed = [10, 0]
        print('headcoll')

    pygame.draw.rect(screen, white, head)
    pygame.draw.rect(screen, green, food)
    pygame.draw.rect(screen, red, wall, 5)


    pygame.display.update()

    fitness = (snake_length + 0.1) * (time.time() - start_time)
    #print('Fitness:', fitness)
    clock.tick(20)




