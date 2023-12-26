import pygame 
import random
import constants

class Border():
    def __init__(self, surface, shift, h):
        self.h = h
        self.surface = surface
        self.shift = shift
        self.x = constants.WIDTH

    def draw(self):
        #initial constants
        self.x = constants.WIDTH + self.shift

        pygame.draw.rect(self.surface, "blue", pygame.Rect(self.x, 0, 1, self.h))
        pygame.draw.rect(self.surface, "blue", pygame.Rect(self.x, constants.HEIGHT-self.h, 1, self.h)) 
        
