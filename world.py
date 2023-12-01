import pygame 
import random
import constants

class World:
    def __init__(self, w, h, surface):
        self.w = w
        self.h = h
        self.surface = surface
        self.color = (255, 100, 100)
        self.s = 0
        self.v = -1
    
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

    def generate(self, x_move):
        #initial constants
        random_length = 100
        randint = random.random()

        if randint > 0.995:
            random_length = random.randrange(100, 200)
        
        pygame.draw.rect(self.surface, "blue", pygame.Rect(constants.WIDTH-x_move, 0, 100, random_length))
        pygame.draw.rect(self.surface, "blue", pygame.Rect(constants.WIDTH-x_move, constants.HEIGHT-random_length, 100, random_length)) 

    def update(self):
        #"scroll" the default screen
        self.s += self.v
        self.default(self.s)

        #"scroll" the old screen


        #generate the new screen

            

