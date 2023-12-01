# Example file showing a basic pygame "game loop"
# hey
import pygame
from world import World
import constants

# pygame setup
pygame.init()

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

world_1 = World(WIDTH, HEIGHT, screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    world_1.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()