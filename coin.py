import pygame

class Coin:
    def __init__(self,x,y,vx):
        self.x = x
        self.y = y
        self.vx = vx
        self.r = 20
        self.alive = True

    def draw(self,screen):
        pygame.draw.circle(screen, "yellow", (self.x,self.y), self.r)
    
    def update(self):
        self.x = self.x + self.vx
        if self.x < 0:
            self.alive = False