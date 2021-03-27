import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()


test_list = [15, 30, 45, 60]
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Draw window for game
pygame.display.set_caption("Tuffy Catches Mangoes") #Title of window

#RGB COLOR CODES----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 15
tuffy_Width, tuffy_Height = 192, 192
MANGO_WIDTH, MANGO_HEIGHT = 80, 80
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load( #Load elephant image
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale( #Change elephant  size
    YELLOW_SPACESHIP_IMAGE, (tuffy_Width, tuffy_Height))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (tuffy_Width, tuffy_Height)), 0)

MANGO_IMAGE = pygame.image.load( #Load the mango
    os.path.join('Assets', 'mango01.png'))
MANGO = pygame.transform.scale( #Take the loaded mango and scale it
    MANGO_IMAGE, (MANGO_WIDTH, MANGO_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load( #Background
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, falling_mangos, red_health, score):
    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    score_text = HEALTH_FONT.render(
        "Health: " + str(score), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(score_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        WIN.blit(MANGO, (bullet.x, bullet.y))

    for bullet in falling_mangos:
        WIN.blit(MANGO, (bullet.x, bullet.y))

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_LEFT] and yellow.x - VEL > 0: # LEFT DASH
        yellow.x -= 1.5*VEL
      
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
      
    if keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < 900: # RIGHT DASH
        yellow.x += 1.5*VEL
       
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL + yellow.width < 900:  # RIGHT
        yellow.x += VEL
  
      
    
   

def handle_bullets(falling_mangos, red_bullets, yellow, red):
    for bullet in falling_mangos:
        bullet.y += BULLET_VEL
        if yellow.colliderect(bullet): #WE CATCH IT
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            falling_mangos.remove(bullet)
        elif bullet.y > 840: #WE DONT CATCH
            falling_mangos.remove(bullet) 

    for bullet in red_bullets:
        bullet.y += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, tuffy_Width, tuffy_Height) #Create a red spaceship
    yellow = pygame.Rect(50, 708, tuffy_Width, tuffy_Height)

    red_bullets = [] #Keep track of our bullets
    falling_mangos = []

    red_health = 10 #Keep track of our health
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(falling_mangos) < MAX_BULLETS:
                    bullet = pygame.Rect(random.randint(0, 820), 0, 80, 80)
                    falling_mangos.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health += 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                score += 1
                #BULLET_HIT_SOUND.play()

        # winner_text = ""
        # if red_health <= 0:
        #    winner_text = "Yellow Wins!"

        # if score <= 0:
        #     winner_text = "Red Wins!"

        # if winner_text != "":
        #    draw_winner(winner_text)
        #     break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
       

        handle_bullets(falling_mangos, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, falling_mangos,
                    red_health, score)

    main()


if __name__ == "__main__":
    main()
