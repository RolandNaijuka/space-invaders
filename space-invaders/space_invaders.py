import pygame
from pygame import mixer

import random
import math


pygame.init()

#create the screen
width = 800
height = 600
screen = pygame.display.set_mode((width,height))

#background
background = pygame.image.load('background.png')

#background music
mixer.music.load("background.wav")
mixer.music.play(-1)


#change title and icon
icon = pygame.image.load('ufo.png')
pygame.display.set_caption("Space Invaders by RolandNaijuka @github")
pygame.display.set_icon(icon)


#Player
player_img = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


#Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(25)
    enemyY_change.append(18)


#Bullet
#ready - you can't see the bullet on the screen
#fire - the bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 65
bullet_state = "ready"


#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

testX = 10
testY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)



def show_score(x,y):
    score = font.render("Score is: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))


def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 37:
        return True
    else:
        return False  



#Game Loop
running = True
while running:
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -20
            if event.key == pygame.K_RIGHT:
                playerX_change = 20
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    #player movements
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    #enemy movements
    for i in range(num_of_enemies):
        #Game Over
        if(enemyY[i] > 480):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 20
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -20
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
            score_value += 1

        enemy(enemyX[i],enemyY[i],i)


    #bullet movements
    if bulletY <= 0:
        bulletY = 480
        bullet_state ="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX,playerY)
    show_score(testX,testY)
    pygame.display.update()