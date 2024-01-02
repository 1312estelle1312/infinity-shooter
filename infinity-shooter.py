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
p = Player(100, HEIGHT/2, 4, 4, 30, "blue", world_1.v, False)
p2 = Player(100, HEIGHT/2, 4, 4, 30, "red", world_1.v, True)

#Coins
c = Coin(WIDTH/1.5, HEIGHT/2)

coins = []

#generate initial borders
for i in range(constants.WIDTH):
    randint = random.random()

    if randint > 0.99:
        height_border = random.randrange(50, 250, 10)    

    new_border = Border(screen, -i, height_border)
    new_border.draw()

    current_elements.append(new_border)


#Hitbox
def collide(x1, y1, x2, y2, r1, r2):
    dx = x2 - x1
    dy = y2 - y1

    if (dx**2 + dy**2) <= ((r1+r2)**2):
        return True    
    
def collide_border_player(player, cl):
    touched = 0
    direction = 0
    for border in range(0, len(cl), 10):
        for i in [*range(0, cl[border].h+1, 10)]+[*range(constants.HEIGHT-cl[border].h, constants.HEIGHT, 10)]:
            if collide(player.x, player.y, cl[border].x, i, player.r-5, 0):
                if player.y < constants.HEIGHT/2:
                    touched = "up"
                elif player.y > constants.HEIGHT/2:
                    touched = "down"
                if touched == "up" and i != cl[border].h or touched == "down" and i != constants.HEIGHT-cl[border].h:
                    if player.x < cl[border].x:
                        direction = "left"
                    elif player.x > cl[border].x:
                        direction = "right" 
                #print(f"t:{touched}, d:{direction}, i:{i}, bord:{cl[border].h}")
    return touched, direction


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

    #Check if player touched border and update
    touched, direction = collide_border_player(p, current_elements)
    p.update(pressed, touched, direction)

    touched, direction = collide_border_player(p2, current_elements) 
    p2.update(pressed, touched, direction)


    if p.alive == False or p2.alive == False:
        running = False
    
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


    #Update bullets if collided  
    new_bullets = []
    for b in bullets:
        if b.alive:
            new_bullets.append(b)
    bullets = new_bullets

    #Update bullets if collided
    new_coins = []
    for c in coins:
        if b.alive:
            new_coins.append(b)
    coins = new_coins

    #Update opponents if collided
    ops = [o for o in ops if o.alive]
    
    #Update coin (REMAKE)
    c.update()
    

    #draw ops, bullets and coins
    p.draw(screen)
    p2.draw(screen)
    for o in ops: 
        o.draw(screen)
    for b in bullets:
        b.draw(screen)
    for c in coins:
        c.draw(screen)

    #"scroll" the old screen 
    new_current_elements = []
    for border in current_elements:
        if border.shift >= constants.WIDTH * -1:
            new_current_elements.append(border)

        border.shift += world_1.v 
        border.draw()
    current_elements = new_current_elements   

    #generate the new screen
    randint = random.random()

    if randint > 0.99:
        height_border = random.randrange(50, 250, 10)    

    new_border = Border(screen, 0, height_border)
    new_border.draw()

    current_elements.append(new_border)

    world_1.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()