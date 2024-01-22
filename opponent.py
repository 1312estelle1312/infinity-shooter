import pygame 
import constants

class Opponent:
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = 30
        self.alive = True

    def draw(self,screen):
        pygame.draw.circle(screen, "red", (self.x, self.y), self.r)
    
    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if self.x < 0:
            self.alive = False