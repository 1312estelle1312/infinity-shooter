import pygame 

class Coin:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.radius = 3

    def draw(self,screen):
        pygame.draw.circle(screen, "gold", (self.x,self.y), self.radius)      
    
    