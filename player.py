import pygame 

class Player:
    def __innit__(self,x,y,vx,vy,r):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.alive = True

    def draw(self,screen):
        pygame.draw.circle(screen, "red", self.x, self.y, self.r)

    def update(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        