import time
import random
from pathlib import Path
import pathlib
from os import listdir

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT


pygame.init()


FPS = pygame.time.Clock()
"""
width, height = 800, 600
screen = width, height
"""
screen = width, height = 800, 600
BLACK = 0, 0, 0

"""
GREY = 155, 155, 155 це був бэкграунд
RED = 255, 0, 0 #додано в уроці 2 це вороги
GREEN = 50, 205, 50 це бонусы

#randomColor = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256) в першому заннятті колір квадратика змінювався рандомно при відскочуванні від стіни
"""

font = pygame.font.SysFont("Verdana", 20)

print(screen)

main_surface = pygame.display.set_mode(screen)
#main_surface.fill( GREY )

"""
#ball = pygame.Surface( (20,20) )
#ball.fill( WHITE )
# запис PLAYER = Path('img', 'player.png')  замінює 2 попередніх рядки
"""
BONUS = Path('img', 'bonus.png')
ENEMY =  Path('img', 'enemy.png')
BONUS  = Path('img', 'bonus.png')
PLAYER = Path('img','player.png')
BACKGROUND = Path('img', 'background.png')

IMGS_PATH = 'img/bandera-goose'

player_imgs = [pygame.transform.scale( pygame.image.load(IMGS_PATH + '/' + file ).convert_alpha(), ( 104, 44) ) for file in listdir( IMGS_PATH ) ]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 10 #less 2


def create_enemy():
    #enemy = pygame.Surface( (20, 20) ) #додано в уроці 2
    #enemy.fill(RED)  #додано в уроці 2
    
    enemy = pygame.transform.scale( pygame.image.load(ENEMY).convert_alpha(), ( 107, 38 ) )
    enemy_rect = pygame.Rect(width, random.randint(0, height-enemy.get_size()[1] ), *enemy.get_size())
    enemy_speed = random.randint(2,5) #less 2
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    """
    #bonus = pygame.Surface( (20, 20) ) #додано в уроці 2
    #bonus.fill(GREEN)  #додано в уроці 2
     """

    bonus = pygame.transform.scale( pygame.image.load(BONUS).convert_alpha(), ( 87, 145 ))
    bonus_rect = pygame.Rect( random.randint(0, width-bonus.get_size()[0]), 0-bonus.get_size()[0], *bonus.get_size()) 
    #0-bonus.get_size()[0]-так бонуси з'являються поступово. Якщо б гусак знаходиться біля межі вікна гри, де з'являється бонус, то бонус просто б блимкнув і пропав, ми навіть і не помітили б його.
    bonus_speed = random.randint(2,5) #less 2
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale( pygame.image.load(BACKGROUND).convert_alpha(), screen) # і видаляємо main_surface.fill( GREY )
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0
scores = 0

enemies = []
bonuses = []


is_working = True


while is_working:
    FPS.tick(40)

    for event in pygame.event.get():
        print(event.type)
        print(event)
        if event.type == QUIT:
           # pygame.quit() #<Event(256-Quit {})>
           is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append( create_enemy() )

        if event.type == CREATE_BONUS:
            bonuses.append( create_bonus() )

        if event.type ==CHANGE_IMG:
            img_index = img_index +1 

            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]  
            

    """
    Частина з уроку 1
    player_rect = player_rect.move(player_speed)

    #randomColor = random.triangular(0, 256, 155), random.triangular(0, 256, 155), random.triangular(0, 256, 155)
    randomColor = random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)

    if player_rect.bottom >= height or player_rect.top <= 0:
        player_speed[1] = -player_speed[1]
        ball.fill( randomColor )

    if player_rect.right >= width or player_rect.left <= 0:
        player_speed[0] = -player_speed[0]
        ball.fill( randomColor )
    """    

    pressed_keys = pygame.key.get_pressed()
    #main_surface.fill( GREY )
    #main_surface.blit( bg, (0,0) )

    bgX = bgX - bg_speed
    bgX2 = bgX2 - bg_speed
    

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()


    main_surface.blit( bg, ( bgX, 0 ) )
    main_surface.blit( bg, ( bgX2, 0 ) )

    main_surface.blit(player, player_rect )

    main_surface.blit( font.render( str(scores), True, BLACK), (width-30, 0 ) )

    for enemy in enemies:
        enemy[1] =  enemy[1].move( -enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop( enemies.index(enemy) )

        if player_rect.colliderect( enemy[1] ):
            #enemies.pop( enemies.index(enemy) ) less 2
            is_working = False #+lesson 3


    for bonus in bonuses:
        bonus[1] =  bonus[1].move( 0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])


        if bonus[1].bottom > height:
            bonuses.pop( bonuses.index(bonus) )

        if player_rect.colliderect( bonus[1] ):
            bonuses.pop( bonuses.index(bonus) ) 
            scores = scores + 1 #такий запис для мене більш зрозумілий

    if pressed_keys[K_DOWN] and player_rect.bottom < height:
        player_rect = player_rect.move(0, player_speed)
    
    if pressed_keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and player_rect.right  < width:
        player_rect = player_rect.move(player_speed, 0)
       
    if pressed_keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(-player_speed, 0)  


    pygame.display.flip()   
    time.sleep(0.006) 




"""
if(...)
{
    ....
}

while(...) { ... }

if ...:
    ...
    ...
    ...
...

"""



"""
print(pygame.event.get())-запуск
результат
[<Event(4352-AudioDeviceAdded {'which': 0, 'iscapture': 0})>, 
<Event(4352-AudioDeviceAdded {'which': 0, 'iscapture': 1})>, 
<Event(32768-ActiveEvent {})>, 
<Event(32774-WindowShown {'window': None})>, 
<Event(32768-ActiveEvent {'gain': 1, 'state': 1})>, 
<Event(32785-WindowFocusGained {'window': None})>, 
<Event(770-TextEditing {'text': '', 'start': 0, 'length': 0, 'window': None})>, 
<Event(32770-VideoExpose {})>, 
<Event(32776-WindowExposed {'window': None})>]
"""