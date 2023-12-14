import pygame 
import random
import constants

class Rects():
    def __init__(self, surface):
        self.h = 100
        self.surface = surface
        self.shift = 0

    def gen_rect(self, shift):
        #initial constants
        randint = random.random()
        self.shift = shift

        if randint > 0.995:
            self.h = random.randrange(100, 200)

        pygame.draw.rect(self.surface, "blue", pygame.Rect(constants.WIDTH+shift-10, 0, 100, self.h))
        pygame.draw.rect(self.surface, "blue", pygame.Rect(constants.WIDTH+shift-10, constants.HEIGHT-self.h, 100, self.h)) 
        
