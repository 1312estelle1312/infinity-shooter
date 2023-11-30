import pygame 
import random

class World:
    def __init__(self, w, h, surface):
        self.w = w
        self.h = h
        self.surface = surface
        self.color = (255, 100, 100)
        self.s = 0
        self.v = -10
    
    def default(self, start_x):
        w3 = self.w/3
        h3 = self.h/3

        #Rect Oben
        pygame.draw.rect(self.surface, self.color, pygame.Rect(0+start_x, 0, w3, h3))
        pygame.draw.rect(self.surface, self.color, pygame.Rect(w3*2+start_x, 0, w3, h3))

        #Rect Unten
        pygame.draw.rect(self.surface, self.color, pygame.Rect(0+start_x, h3*2, w3, h3))   
        pygame.draw.rect(self.surface, self.color, pygame.Rect(w3*2+start_x, h3*2, w3, h3)) 

        #Rect oben und unten in der Mitte
        pygame.draw.rect(self.surface, self.color, pygame.Rect(w3+start_x, 0, round(w3), h3/2))
        pygame.draw.rect(self.surface, self.color, pygame.Rect(w3+start_x, h3*2.5, round(w3), h3/2,)) 

    def update(self):

        random_length = random.randrange(100, 200)
        random_width = random.randrange(100, 200)

        #"scroll" the old screen
        self.s += self.v
        self.default(self.s)

