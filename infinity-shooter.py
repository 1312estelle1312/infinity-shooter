# Example file showing a basic pygame "game loop"
# hey
import pygame
from world import World
import constants
from rects import Rects


# pygame setup
pygame.init()

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
current_elements = []

world_1 = World(WIDTH, HEIGHT, screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    world_1.update()

    #generate the new screen
    new_rect = Rects(screen)
    new_rect.gen_rect(0)
    #print(new_rect.shift)

    current_elements.append(new_rect)
    #print(current_elements)

    #"scroll" the old screen
    for rect in current_elements:
        if rect.shift <= constants.WIDTH * -1:
            current_elements.remove(rect)
        rect.gen_rect(world_1.s)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()