import pygame
import random
from player import Player
from bullet import Bullet
from opponent import Opponent

pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

screen.fill((0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()