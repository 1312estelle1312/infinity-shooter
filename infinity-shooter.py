# Example file showing a basic pygame "game loop"
# hey
import pygame
import random
from world import World
import constants
from border import Border
import random
from coin import Coin
from opponent import Opponent
from player import Player
from bullet import Bullet

# pygame setup
pygame.init()

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
current_elements = []

world_1 = World(WIDTH, HEIGHT, screen)
height_border = 100

#For border
touched = False

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
p = Player(100, HEIGHT/2, 4, 4, 30, world_1.v)

#Coins
c = Coin(WIDTH/1.5, HEIGHT/2)

coins = []

#Hitbox
def collide(x1, y1, x2, y2, r1, r2):
    dx = x2 - x1
    dy = y2 - y1

    if (dx**2 + dy**2) < ((r1+r2)**2):
        return True    

def collide_border_player(player):
    for border in current_elements:
        for i in range(border.h):
            collide(player.x, player.y, border.x, i, p.r, 0)

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
    screen.fill((70, 100, 30))

    #Check if player touched
    touched = False
    if collide_border_player(p):
        touched = True   

    #Update if player or bullets touched
    p.update(pressed, touched)
    for o in ops:
        o.update()
    for b in bullets:
        b.update()

    #Check if opponent and bullets collide
    for opponent in ops:
        for bullet in bullets:
            if collide(opponent.x, opponent.y, bullet.x, bullet.y, opponent.radius, bullet.radius):
                opponent.alive = False
                bullet.alive = False
    
    #Check if oppent and coins collide (REMAKE)
        for coin in coins:
            if collide(coin.x, coin.y, bullet.x, bullet.y, bullet.radius, coin.radius):
                coin.alive = False


    #Update bullets      
    new_bullets = []
    for b in bullets:
        if b.alive:
            new_bullets.append(b)
    bullets = new_bullets

    #Update bullets
    new_coins = []
    for c in coins:
        if b.alive:
            new_coins.append(b)
    coins = new_coins

    #Update opponents
    ops = [o for o in ops if o.alive]
    
    #Update coin (REMAKE)
    c.update()

    #"scroll" the old screen
    for border in current_elements:
        if border.shift <= constants.WIDTH * -1:
            current_elements.remove(border)

        border.shift += world_1.v 
        border.draw()


    #generate the new screen
    randint = random.random()

    if randint > 0.99:
        height_border = random.randrange(50, 250)    

    new_border = Border(screen, 0, height_border)
    new_border.draw()

    current_elements.append(new_border)

    world_1.update()

    #draw ops, bullets and coins
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