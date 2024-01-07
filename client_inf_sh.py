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
from network import Network

# pygame setup
pygame.init()
pygame.display.set_caption("Client")

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT

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
 
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_screen = True

    n = Network()
    local_list = n.connect()
    ready_state = "not_ready"

    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_screen = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                ready_state = "ready"

        ready_state_other = n.send_and_get(ready_state)
        
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 40)

        if (ready_state == "ready" and ready_state_other == "ready") or ready_state_other == "done":
            start_button = font.render("Start [Press Enter]", True, (255, 255, 255))
            screen.blit(start_button, (constants.WIDTH/2 - start_button.get_width()/2, constants.HEIGHT/2 + start_button.get_height()/2))
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or ready_state_other == "done":
                ready_state_other = n.send_and_get("done")
                for i in range(5):
                    #print(5-i)
                    screen.fill((0, 0, 0))
                    countdown = font.render(f"Game starts in: {5-i}", True, (255, 255, 255))
                    screen.blit(countdown, (constants.WIDTH/2 - countdown.get_width()/2, constants.HEIGHT/2 - 4 * countdown.get_height()/2))
                    pygame.display.update()
                    pygame.time.wait(1000)
                    #print(p.x)
                start_screen = False
                game(n, local_list)

        title = font.render("Infinity Shooter", True, (255, 255, 255))
        ready_button = font.render("Ready [Press R]", True, (255, 255, 255))

        screen.blit(title, (constants.WIDTH/2 - title.get_width()/2, constants.HEIGHT/2 - title.get_height()/2))
        screen.blit(ready_button, (constants.WIDTH/2 - ready_button.get_width()/2, constants.HEIGHT/2 + 3*ready_button.get_height()/2))
        pygame.display.update()

def game_over_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    end_screen = True

    #Network handling
    #n = Network()


    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                end_screen = False
                game()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                end_screen = False
                pygame.quit()
        
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        screen.blit(title, (constants.WIDTH/2 - title.get_width()/2, constants.HEIGHT/2 - title.get_height()/3))
        screen.blit(restart_button, (constants.WIDTH/2 - restart_button.get_width()/2, constants.HEIGHT/1.9 + restart_button.get_height()))
        screen.blit(quit_button, (constants.WIDTH/2 - quit_button.get_width()/2, constants.HEIGHT/2 + quit_button.get_height()/2))
        pygame.display.update()

def game(n, local_list):
    #initial settings
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    current_elements = []

    world_1 = World(WIDTH, HEIGHT, screen)
    height_border = 100

    p = local_list[0]
    bullets = local_list[1]
    ops = local_list[2]


    #Liste für Bullets
    #bullets = []

    #Spieler
    #p = Player(100, HEIGHT/2, 4, 4, 30, "blue", world_1.v, False)
    #p2 = Player(100, HEIGHT/2, 4, 4, 30, (118, 31, 184), world_1.v, True)

    #Coins
    c = Coin(WIDTH/1.5, HEIGHT/2)

    coins = []

    #Network handling
    #n = Network()
    #n.connect()

    #generate initial borders
    for i in range(constants.WIDTH):
        randint = random.random()
        random.seed(10)

        if randint > 0.99:
            height_border = random.randrange(50, 250, 10)    

        new_border = Border(screen, -i, height_border)
        new_border.draw()

        current_elements.append(new_border)

    running = True
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

        #Network player and bullets
        local_list = [p, bullets, ops]
        remote_list = n.send_and_get(local_list)
        
        p2 = remote_list[0]
        bullets2 = remote_list[1]
        ops = remote_list[2]


        #print(f"Ops: {len(ops)}")


        #Check if player touched border and update
        touched, direction = collide_border_player(p, current_elements)
        p.update(pressed, touched, direction)

        #print(p2.x) REMAKE
        #touched, direction = collide_border_player(p2, current_elements) 
        #p2.update(pressed, touched, direction)


        if p.alive == False or p2.alive == False:
            game_over_state = n.send_and_get("game_over")
            running = False
            game_over_screen()
    

        for o in ops:
            o.update()
        for b in bullets:
            b.update()
        for b in bullets2:
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

        #Update coins if collided
        new_coins = []
        for c in coins:
            if b.alive:
                new_coins.append(b)
        coins = new_coins

        #Update opponents if collided
        new_opponents = []
        for opponent in ops:
            if opponent.alive:
                new_opponents.append(opponent)
        ops = new_opponents
        
        #Update coin (REMAKE)
        c.update()
        

        #draw ops, bullets and coins
        p.draw(screen)
        p2.draw(screen)
        for o in ops: 
            o.draw(screen)
        for b in bullets:
            b.draw(screen)
        for b in bullets2:
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
        #Print FPS if you want
        #print(clock.get_fps())


main_menu()