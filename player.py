import pygame 

class Player:
    def __init__(self,x,y,vx,vy,r):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.alive = True

    def draw(self,screen):
        pygame.draw.circle(screen, "blue", (self.x, self.y), self.r)

    def update(self, pressed):
        if pressed[pygame.K_w]:
            self.y -= self.vy
        elif pressed[pygame.K_s]:
            self.y += self.vy
        if pressed[pygame.K_a]:
            self.x -= self.vx
        elif pressed[pygame.K_d]:
            self.x += self.vx
    