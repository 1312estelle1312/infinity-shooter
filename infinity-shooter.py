# Example file showing a basic pygame "game loop"
# hey
import pygame
import random
from world import World
from coin import Coin
from opponent import Opponent
from player import Player
from bullet import Bullet




# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

world_1 = World(WIDTH, HEIGHT, screen)

#Liste für Gegner
ops = []
for _ in range(10):
    x = random.randint(426, 853)
    y = random.randint (240, 480)
    vx = random.randint (-1, 0)
    vy = random.randint (-1, 0)
    opponent = Opponent(x,y,vy,vx)
    ops.append(opponent)
#Liste für Bullets
bullets = []

#Spieler
p = Player(100, HEIGHT/2, 4, 4, 30)

#Hitbox
def collides(o,b):
    dx = o.x - b.x
    dy = o.y - b.y
    radii = o.radius + b.radius
    if (dx * dx + dy * dy) < (radii * radii):
        print("Down")
        return True
    else:
        return False
c = Coin(WIDTH/1.5, HEIGHT/2)

coins = []
 #Hitbox Coin
def collides(p,c):
    dx = p.x - c.x
    dy = p.y - c.y
    radii = p.radius + c.radius
    if (dx * dx + dy * dy) < (radii * radii):
        print("+1")
        return True
    else:
        return False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Shots
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            b = Bullet(p.x ,p.y - p.r + 25, 15)
            bullets.append(b) 
    
    pressed = pygame.key.get_pressed()
    # UPDATE:
    p.update(pressed)
    for o in ops:
        o.update()
    for b in bullets:
        b.update()


    for opponent in ops:
        for bullet in bullets:
            if collides(opponent,bullet):
                opponent.alive = False
                bullet.alive = False
    
    
        for coin in coins:
            if collides(coin):
                coin.alive = False
            
    new_bullets = []
    for b in bullets:
        if b.alive:
            new_bullets.append(b)
    bullets = new_bullets

    new_coins = []
    for c in coins:
        if b.alive:
            new_coins.append(b)
    coins = new_coins

    ops = [o for o in ops if o.alive]
    
    c.update()

    screen.fill((0, 0, 0))

    world_1.update()

    p.draw(screen)
    for o in ops: 
        o.draw(screen)
    for b in bullets:
        b.draw(screen)
    for c in coins:
        c.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()