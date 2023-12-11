import pygame 
import random
import constants

class Rects():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def gen_rect(self):
        #initial constants
        self.h = 100
        randint = random.random()

        if randint > 0.995:
            self.h = random.randrange(100, 200)

        pygame.draw.rect(self.surface, "blue", pygame.Rect(self.x, 0, 100, self.h))
        pygame.draw.rect(self.surface, "blue", pygame.Rect(self.x, constants.HEIGHT-self.h, 100, self.h)) 
        
