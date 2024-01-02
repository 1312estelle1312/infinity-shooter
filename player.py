import pygame 


class Player:
    def __init__(self,x,y,vx,vy,r, world_v):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.alive = True
        self.world_v = world_v


    def draw(self,screen):
        pygame.draw.circle(screen, "blue", (self.x, self.y), self.r)

    def update(self, pressed, touched, direction):
            if pressed[pygame.K_w]:
                if touched != "up":
                    self.y = self.y - self.vy 
            elif pressed[pygame.K_s]:
                if touched != "down":
                    self.y = self.y + self.vy
            if pressed[pygame.K_a]:
                if direction != "right":
                    self.x -= self.vx
            elif pressed[pygame.K_d]:
                if direction != "left":
                    self.x += self.vx
            if direction == "left":
                self.x += self.world_v    
    