import pygame

class Healthbar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    
    def draw(self, screen):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, "white", (self.x - 4, self.y - 4, self.w + 8, self.h + 8))
        pygame.draw.rect(screen, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, "green", (self.x, self.y, self.w * ratio, self.h))