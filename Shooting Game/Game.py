# Making a basic game using pygame module

import pygame # importing the pygame module
import os #importing os to set the path to our assets
from pygame.constants import RESIZABLE
from pygame.draw import line # RESIZABLE helps to resize the window
pygame.font.init()
pygame.mixer.init()

# setting the height and the width of the gaming window
WIDTH, HEIGHT = 900, 500
size=(WIDTH, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT= 55, 40

YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2

# Making a screen passing the scren size and whether we want it to be resizable or not
WIN = pygame.display.set_mode(size, RESIZABLE)
# this one sets the title on the gaming window
pygame.display.set_caption("First Game!")

# initializing the color tuple and FPS
SWINE=(23,255,255)
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT=pygame.font.SysFont('comicsans', 40)
WINNER_FONT=pygame.font.SysFont('comicsans', 100)

FPS=60
VEL=5
BULLET_VEL=7
MAX_BULLETS=3

# reading the image files using setting path by os to make it operating system independent and resizing them
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP=pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP=pygame.transform.rotate(YELLOW_SPACESHIP,90)

RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP=pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP=pygame.transform.rotate(RED_SPACESHIP,270)

SPACE=pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE=pygame.transform.scale(SPACE, size)

# the function is to draw on how the window looks from inside
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # order in which we draw things matter if we fill the screen after deploying the spaceship we wont see the screen

    # fill the window with the passed color
    # WIN.fill(SWINE)
    WIN.blit(SPACE, (0,0))
    # helps to draw the rectangle taking, first argument is the window on which we will be drawing it and then color and the rectangle which we wish to draw
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1, SWINE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1, SWINE)
    WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # WE use blit when we want to draw a surface on a screen
    # here we are drawing spaceship image and we signify the coordinate where top to bottom is positive
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # we need to update the display after we do some change or else the change doesn't get deployed
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if(keys_pressed[pygame.K_a] and yellow.x-VEL>0): #LEFT
        yellow.x-=VEL
    if(keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x): #Right
        yellow.x+=VEL
    if(keys_pressed[pygame.K_w] and yellow.y-VEL>0): #UP
        yellow.y-=VEL
    if(keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height <HEIGHT-10): #Down
        yellow.y+=VEL
    
def red_handle_movement(keys_pressed, red):
    if(keys_pressed[pygame.K_LEFT] and red.x-VEL >BORDER.x + BORDER.width): #LEFT
        red.x-=VEL
    if(keys_pressed[pygame.K_RIGHT] and red.x+VEL+ red.width<WIDTH): #Right
        red.x+=VEL
    if(keys_pressed[pygame.K_UP] and red.y-VEL>0): #UP
        red.y-=VEL
    if(keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height <HEIGHT-10): #Down
        red.y+=VEL

def handle_bullets(yellow_bulllets, red_bullets, yellow, red):
    for bullet in yellow_bulllets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bulllets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bulllets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text=WINNER_FONT.render(text, 1, SWINE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()/2, HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

# this is a main method where we intend to tackle all the changes
def main():
    yellow=pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red=pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets=[]
    yellow_bullets=[]
    red_health=5
    yellow_health=5
    # this is to create an object clock to controll the running rate of the while loop
    clock = pygame.time.Clock()
    run= True
    # we run this loop which means our game is in continuous execution
    while(run):
        # setting our FPS
        clock.tick(FPS)
        # we are fetchin the any event of importance 
        for event in pygame.event.get():
            # if the event is a Quit event we simply just make the while loop stop
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if(event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS):
                    bullet=pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if(event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS):
                    bullet=pygame.Rect(red.x, red.y+red.height//2-2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()

            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

        winner_text=""
        if(red_health<=0):
            winner_text="Yellow Wins!"
        if(yellow_health<=0):
            winner_text="Red Wins!"
        if winner_text!="":
            draw_winner(winner_text)
            break
        # tells us what keys are being pressed out and if the key is being pressed down it will register that the key is being pressed for a long time
        # print(red_bullets, yellow_bullets)
        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)



        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    # to restart down the program 
    main()


if __name__=="__main__":
    main()
    