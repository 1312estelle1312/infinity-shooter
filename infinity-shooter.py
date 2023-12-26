# Example file showing a basic pygame "game loop"
# hey
import pygame
from world import World
import constants
from border import Border
import random


# pygame setup
pygame.init()

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
current_elements = []

world_1 = World(WIDTH, HEIGHT, screen)
height_border = 100

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    #"scroll" the old screen

    for border in current_elements:
        if border.shift <= constants.WIDTH * -1:
            current_elements.remove(border)

        border.shift += world_1.v 
        border.draw()


    #generate the new screen
    randint = random.random()

    if randint > 0.95:
        height_border = random.randrange(100, 200)    

    new_border = Border(screen, 0, height_border)
    new_border.draw()

    current_elements.append(new_border)
    #print(current_elements)


    world_1.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()