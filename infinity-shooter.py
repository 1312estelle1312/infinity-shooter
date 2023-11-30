import pygame
import random
from opponent import Opponent
from player import Player
from bullet import Bullet

# pygame setup
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")
clock = pygame.time.Clock()
running = True
aliens = []
for _ in range(20):
    x = random.randint(20, WIDTH-20)
    y = random.randint (-200, -20)
    vy = random.randint (2,4)
    alien = Alien(x,y,vy)
    aliens.append(alien)
bullets = []

p = Player(WIDTH/2, HEIGHT - 100, 4, 4)

def collides(a,b):
    dx = a.x - b.x
    dy = a.y - b.y
    radii = a.radius + b.radius
    if (dx * dx + dy * dy) < (radii * radii):
        print("sdfgsdfg")
        return True
    else:
        return False

while running:
    # EVENT HANDLING:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            b = Bullet(p.x ,p.y - p.radius, -6)
            bullets.append(b)

    pressed = pygame.key.get_pressed()

    

    # UPDATE:
    p.update(pressed)
    for a in aliens:
        a.update()
    for b in bullets:
        b.update()


    for alien in aliens:
        for bullet in bullets:
            if collides(alien,bullet):
                alien.alive = False
                bullet.alive = False
    
    new_bullets = []
    for b in bullets:
        if b.alive:
            new_bullets.append(b)
    bullets = new_bullets

    aliens = [a for a in aliens if a.alive]
    
    # DRAW:
    screen.fill((0, 0, 0))

    p.draw(screen)
    for a in aliens: 
        a.draw(screen)
    for b in bullets:
        b.draw(screen) 
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()