# Example file showing a basic pygame "game loop"
# hey
import pygame
import random
from world import World
import constants
from border import Border
import random
from opponent import Opponent
from player import Player
from bullet import Bullet
from network import Network

# pygame setup
pygame.init()
pygame.display.set_caption("Client")

WIDTH = constants.WIDTH
HEIGHT = constants.HEIGHT

font = pygame.font.SysFont(None, 40)
bg = pygame.image.load("static/bg.jpg")
bg = pygame.transform.scale(bg, ((WIDTH, HEIGHT)))

pic_player = pygame.image.load("static/picp.png")
pic_player = pygame.transform.scale(pic_player, ((60, 60)))

pic_op = pygame.image.load("static/tiger.png")
pic_op = pygame.transform.scale(pic_op, ((60, 60)))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

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

def changed(l, l_old):
    pass
    
def menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu_screen = True
    while menu_screen:
 
        screen.fill((81, 79, 97))
        draw_text('Main Menu', font, (255, 255, 255), screen, WIDTH/2-85, 40)
 
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(WIDTH/2-100, HEIGHT/2-50, 250, 50)
        button_2 = pygame.Rect(WIDTH/2-100, HEIGHT/2+50, 250, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                menu_screen = False
                game(0, False, 0)
        if button_2.collidepoint((mx, my)):
            if click:
                menu_screen = False
                main_menu()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
 
        #writing text on top of button
        draw_text('SINGLEPLAYER', font, (255,255,255), screen, WIDTH/2-85, HEIGHT/2-50+15)
        draw_text('MULTIPLAYER', font, (255,255,255), screen, WIDTH/2-85, HEIGHT/2+50+15)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()


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

        screen.fill((81, 79, 97))
        font = pygame.font.SysFont(None, 40)

        if (ready_state == "ready" and ready_state_other == "ready") or ready_state_other == "done":
            start_button = font.render("Start [Press Enter]", True, (255, 255, 255))
            screen.blit(start_button, (constants.WIDTH/2 - start_button.get_width()/2, constants.HEIGHT/2 + start_button.get_height()/2))
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or ready_state_other == "done":
                ready_state_other = n.send_and_get("done")
                for i in range(5):
                    #print(5-i)
                    screen.fill((81, 79, 97))
                    countdown = font.render(f"Game starts in: {5-i}", True, (255, 255, 255))
                    screen.blit(countdown, (constants.WIDTH/2 - countdown.get_width()/2, constants.HEIGHT/2 - 4 * countdown.get_height()/2))
                    pygame.display.update()
                    pygame.time.wait(1000)
                    #print(p.x)
                start_screen = False
                game(n, True, local_list)

        title = font.render("Infinity Shooter", True, (255, 255, 255))
        ready_button = font.render("Ready [Press R]", True, (255, 255, 255))

        screen.blit(title, (constants.WIDTH/2 - title.get_width()/2, constants.HEIGHT/2 - title.get_height()/2))
        screen.blit(ready_button, (constants.WIDTH/2 - ready_button.get_width()/2, constants.HEIGHT/2 + 3*ready_button.get_height()/2))
        pygame.display.update()
        #Highscore print

def game_over_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    end_screen = True

    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                end_screen = False
                menu()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                end_screen = False
                pygame.quit()
        
        screen.fill((81, 79, 97))
        font = pygame.font.SysFont(None, 40)
        title = font.render('Game Over', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        screen.blit(title, (constants.WIDTH/2 - title.get_width()/2, constants.HEIGHT/2 - title.get_height()/3))
        screen.blit(restart_button, (constants.WIDTH/2 - restart_button.get_width()/2, constants.HEIGHT/1.9 + restart_button.get_height()))
        screen.blit(quit_button, (constants.WIDTH/2 - quit_button.get_width()/2, constants.HEIGHT/2 + quit_button.get_height()/2))
        pygame.display.update()


def game(n, multiplayer, local_list):
    #initial settings
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    current_elements = []

    world_1 = World(WIDTH, HEIGHT, screen)
    height_border = 100
    highscore = 0

    if multiplayer:
        p = local_list[0]
        bullets = local_list[1]
        ops = local_list[2]
        game_over_state = local_list[3]
        #worlds

    number_length = 0.5

    if not multiplayer:
        p = Player(100, constants.HEIGHT/2, 4, 4, 30, "blue", -2, False)
        bullets = []
        ops = []
        for _ in range(4):
            x = random.randint(426, 853)
            y = random.randint (240, 480)
            vx = random.randint (-1, 0)
            vy = random.uniform(-0.5, 0)
            opponent = Opponent(x,y,vx,vy)
            ops.append(opponent)
       


    #generate initial borders
    for i in range(constants.WIDTH):
        randint = random.random()
        random.seed(10)

        if randint > 0.99:
            height_border = random.randrange(50, 250, 10)    

        new_border = Border(screen, -i, height_border)
        new_border.draw()

        current_elements.append(new_border)

    game_over_state = False

    ops_new = []

    ops2_old = []

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
        screen.blit(bg, (0, 0))

        #Network player and bullets
        if multiplayer:
            local_list = [p, bullets, ops, game_over_state, world_1.s]
            remote_list = n.send_and_get(local_list)

            if remote_list[3][0]:
                running = False
                n.disconnect()
                game_over_screen()
                continue

            ops2_old = ops[:]

            p2 = remote_list[0]
            bullets2 = remote_list[1]
            ops2 = remote_list[2]
            world2s = remote_list[4]

            #syn world shifts
            world_1.s = world2s

            #synchronize ops
            if len(ops2) < len(ops):
                ops = ops2[:]

            print(world_1.s*-1, WIDTH*number_length)
            ops_new = []
            if world_1.s*-1 <= WIDTH*number_length+10 and world_1.s*-1 >= WIDTH*number_length-10:
                for _ in range(6):
                    x = random.randint(1000, 1150)
                    y = random.randint (240, 480)
                    vx = random.uniform (-1*((world_1.s*-1/WIDTH)*9), 0)
                    vy = random.uniform (-0.5, 0)
                    opponent = Opponent(x,y,vx,vy)
                    ops_new.append(opponent)  
                if number_length >= 2:
                    for _ in range(3):
                        x = random.randint(0, 150)
                        y = random.randint (240, 480)
                        vx = random.uniform (1*((world_1.s*-1/WIDTH)*2), 0)
                        vy = random.uniform (-6, 0)
                        opponent = Opponent(x,y,vx,vy)
                        ops_new.append(opponent) 
                number_length = number_length + 0.5 

        if not multiplayer:
            if world_1.s*-1 == WIDTH*number_length:
                for _ in range(6):
                    x = random.randint(1000, 1150)
                    y = random.randint (240, 480)
                    vx = random.uniform (-1*((world_1.s*-1/WIDTH)*9), 0)
                    vy = random.uniform (-0.5, 0)
                    opponent = Opponent(x,y,vx,vy)
                    ops.append(opponent)  
                if number_length >= 2:
                    for _ in range(3):
                        x = random.randint(0, 150)
                        y = random.randint (240, 480)
                        vx = random.uniform (1*((world_1.s*-1/WIDTH)*2), 0)
                        vy = random.uniform (-6, 0)
                        opponent = Opponent(x,y,vx,vy)
                        ops.append(opponent) 
                number_length = number_length + 0.5 


        #Check if player touched border and update
        touched, direction = collide_border_player(p, current_elements)
        p.update(pressed, touched, direction)

        #Check if opponents touched border and update
        for op in ops:
            touched, direction = collide_border_player(op, current_elements)
            if touched == "up" or touched == "down":
                op.vy = op.vy * -1
            
        #Check if opponents and player touch
        for op in ops:
            if collide(op.x, op.y, p.x, p.y, op.r, p.r):
                p.health = p.health - 1
                op.alive = False


        if p.alive == False:
            if multiplayer:
                game_over_state = True
                continue
            running = False
            game_over_screen()

        for o in ops:
            o.update()
        for b in bullets:
            b.update()

        if multiplayer:
            for b in bullets2:
                b.update()

        #Check if opponent and bullets collide
        for opponent in ops:
            for bullet in bullets:
                if collide(opponent.x, opponent.y, bullet.x, bullet.y, opponent.r, bullet.r):
                    opponent.alive = False
                    bullet.alive = False
                    highscore += 1          
            
        #highscore
        text = font.render(f"Highscore: {highscore}", True, (255,255,255))
        screen.blit(text, (10, 10))


        #Update bullets if collided  
        new_bullets = []
        for b in bullets:
            if b.alive:
                new_bullets.append(b)
        bullets = new_bullets



        #Update opponents if collided
        new_opponents = []
        for opponent in ops:
            if opponent.alive:
                new_opponents.append(opponent)
        ops = new_opponents

        #draw ops, bullets and coins
        p.draw(screen)
        screen.blit(pic_player, (p.x-p.r, p.y-p.r))

        if multiplayer:
            p2.draw(screen)
            screen.blit(pic_player, (p2.x-p2.r, p2.y-p2.r))
        for o in ops: 
            o.draw(screen)
            screen.blit(pic_op, (o.x-o.r, o.y-o.r))
        for b in bullets:
            b.draw(screen)
        if multiplayer:
            for b in bullets2:
                b.draw(screen)


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
        
        #highscore
        text = font.render(f"score: {highscore}", True, (255,255,255))
        screen.blit(text, (10, 10))
        world_1.update()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
        #Print FPS if you want
        #print(clock.get_fps())


menu()