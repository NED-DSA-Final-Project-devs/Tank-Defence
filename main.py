import pygame
import os
from random import randint
from constants import WIDTH, HEIGHT, FPS, PLAYER_VEL, ENEMY_VEL, BULLETS_VEL, INITIAL_WAVE, BLACK, WHITE, GREEN, GREY
from cannon import Cannon
from tank import Tank
from helpers import collide, draw_healthbar, draw_track


pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Defence")
CLOCK = pygame.time.Clock()  # to limit framerate


## Load images
BG = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "bg_1.png")), (WIDTH, HEIGHT))  # Background image

TRACK = pygame.image.load(os.path.join('assets', 'Track_1_A.png'))  # player's tracks
TRACK = pygame.transform.smoothscale(TRACK, (int(TRACK.get_width()*0.5), int(TRACK.get_height()*0.5)))  # scale down to 50 percent of original
TRACK = pygame.transform.rotate(TRACK, 90)  # rotate by 90 degrees

CANNON_IMG = pygame.image.load(os.path.join('assets', 'Gun_01.png'))
CANNON_IMG = pygame.transform.smoothscale(CANNON_IMG, (int(CANNON_IMG.get_width()*0.6), int(CANNON_IMG.get_height()*0.6)))  # scale down to 60 percent of original

TANK_IMG = pygame.image.load(os.path.join("assets", "M-6_preview.png"))
TANK_IMG = pygame.transform.smoothscale(TANK_IMG, (int(TANK_IMG.get_width()*0.45), int(TANK_IMG.get_height()*0.45))) # scale down to 45 percent of original

CANNON_BULLET = pygame.image.load(os.path.join('assets', 'Heavy_Shell.png'))
CANNON_BULLET = pygame.transform.smoothscale(CANNON_BULLET, (int(CANNON_BULLET.get_width()*0.7), int(CANNON_BULLET.get_height()*0.7)))  # scale down to 70 percent of original

TANK_BULLET = pygame.image.load(os.path.join('assets', 'Medium_Shell.png'))
TANK_BULLET = pygame.transform.rotate(TANK_BULLET, 180)



def play():
    run = True
    stats_font = pygame.font.SysFont("arial", 30)
    lost_label = pygame.font.SysFont("arial", 90).render("You Lost!!", 1, WHITE)
    level = 0

    enemies = []
    wave_size = 0  # number of enemies in a level

    player_cannon = Cannon((WIDTH/2 - CANNON_IMG.get_width()/2, HEIGHT*0.81), vel=PLAYER_VEL, image=CANNON_IMG, bullet_image=CANNON_BULLET)

    lost = False
    lost_time = 0

    def update_window():
        level_label = stats_font.render(f"Level: {level}", 1, WHITE)
        health_label = stats_font.render(f"Health", 1, WHITE)
        
        WINDOW.blit(BG, (0, 0))  # background image
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))  # level text
        WINDOW.blit(health_label, (10, 10))  # health text
        draw_healthbar(WINDOW, player_cannon)
        draw_track(WINDOW, TRACK)  # cannon track
        for enemy in enemies:  # draw enemies
            enemy.draw(WINDOW) 
        player_cannon.draw(WINDOW)  # cannon
        
        if lost:
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT*1/5))

        pygame.display.update()  # make the latest changes appear on screen



    while run:
        CLOCK.tick(FPS)
        update_window()

        if player_cannon.get_health() <= 0:
            lost = True
            lost_time += 1

        if lost:
            if lost_time > (FPS * 3):  # if lost for 3 seconds (to show the lost message for 3 seconds)
                run = False
            else:
                continue

        if len(enemies) == 0:  # if all enemies of current level are destroyed
            print(f"Wavesize: {wave_size}, level={level}")
            level += 1
            wave_size += INITIAL_WAVE
            for i in range(wave_size):
                enemy = Tank((randint(0, WIDTH-TANK_IMG.get_width()), randint(-HEIGHT, -HEIGHT//4)), ENEMY_VEL, TANK_IMG, TANK_BULLET)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        # keys for moving left/right
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            if player_cannon.get_x() + player_cannon.get_width() + PLAYER_VEL <= WIDTH:  # check for right edge
                player_cannon.move(PLAYER_VEL)  # move right by PLAYER_VEL units
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            if player_cannon.get_x() - PLAYER_VEL >= 0:  # check for left edge
                player_cannon.move(-PLAYER_VEL)  # move left by PLAYER_VEL units

        # Key for shooting
        if keys_pressed[pygame.K_SPACE]:
            player_cannon.shoot()

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_bullets(BULLETS_VEL, player_cannon)

            if collide(enemy, player_cannon):
                player_cannon.reduce_health()
                enemies.remove(enemy)

            elif enemy.get_y() > HEIGHT:
                player_cannon.reduce_health()  #TODO: health or lives?
                enemies.remove(enemy)
                
            # make enemies shoot at random times
            if randint(0, FPS*2) == 1:
                enemy.shoot()
            

        player_cannon.move_bullets(-BULLETS_VEL, enemies)

    

def main_menu():
    btn_padding = 10
    run = True
    menu_font_1 = pygame.font.SysFont("comicsansms", 100)
    menu_font_2 = pygame.font.SysFont("arial", 35)
    menu_font_3 = pygame.font.SysFont("arial", 23)

    title_label = menu_font_1.render("Tank Defence", 1, WHITE)

    instructions_1 = "Instructions: You are being attacked by tanks."
    instructions_2 = "Move your cannon using 'a' and 'd' keys or right and left arrow keys."
    instructions_3 = "Press spacebar to shoot."
    instructions_4 = "You will have to shoot down all enemies in a level to move to the next level."
    instructions_5 = "You will lose health every time a bullet hits you, an opponent tank collides "
    instructions_6 = "with you or opponent tank goes past you. The game gets over when your health"
    instructions_7 = "becomes zero (health bar will be displayed on top left of screen when you start the game)."
    instructions_label_1 = menu_font_3.render(instructions_1, 1, WHITE)
    instructions_label_2 = menu_font_3.render(instructions_2, 1, WHITE)
    instructions_label_3 = menu_font_3.render(instructions_3, 1, WHITE)
    instructions_label_4 = menu_font_3.render(instructions_4, 1, WHITE)
    instructions_label_5 = menu_font_3.render(instructions_5, 1, WHITE)
    instructions_label_6 = menu_font_3.render(instructions_6, 1, WHITE)
    instructions_label_7 = menu_font_3.render(instructions_7, 1, WHITE)

    begin_label = menu_font_2.render("Play", 1, BLACK)
    begin_button = begin_label.get_rect()
    begin_button.x = WIDTH/2 - begin_label.get_width()/2 - btn_padding
    begin_button.y = HEIGHT*(5/6) - btn_padding
    begin_button.width += btn_padding * 2
    begin_button.height += btn_padding * 2

    
    while run:
        WINDOW.fill(GREY)
        
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT*(1/10)))  # draw game title text
        
        # draw instructions text
        WINDOW.blit(instructions_label_1, (WIDTH/2 - instructions_label_1.get_width()/2, HEIGHT*(2/5)))
        WINDOW.blit(instructions_label_2, (WIDTH/2 - instructions_label_2.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()))
        WINDOW.blit(instructions_label_3, (WIDTH/2 - instructions_label_3.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()*2))
        WINDOW.blit(instructions_label_4, (WIDTH/2 - instructions_label_4.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()*3))
        WINDOW.blit(instructions_label_5, (WIDTH/2 - instructions_label_5.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()*5))
        WINDOW.blit(instructions_label_6, (WIDTH/2 - instructions_label_6.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()*6))
        WINDOW.blit(instructions_label_7, (WIDTH/2 - instructions_label_7.get_width()/2, HEIGHT*(2/5)+instructions_label_1.get_height()*7))

        pygame.draw.rect(WINDOW, GREEN, begin_button, border_radius=10)  # draw play button
        WINDOW.blit(begin_label, (WIDTH/2 - begin_label.get_width()/2, HEIGHT*(5/6)))  # draw play button text on button

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed
                if begin_button.collidepoint(event.pos):  # if mouse pressed on button
                    play()  # start the game

    pygame.quit()




main_menu()
