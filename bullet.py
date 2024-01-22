import pygame

class Bullet:
    def __init__(self,x,y,vx):
        self.x = x
        self.y = y
        self.vx = vx
        self.r = 6
        self.alive = True

    def draw(self,screen):
        pygame.draw.circle(screen, "red", (self.x,self.y), self.r)
    
    def update(self):
        self.x = self.x + self.vx
        if self.x < 0:
            self.alive = False