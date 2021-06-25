import pygame, random, math
from pygame import mixer
# initializing
pygame.init()

screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("space.jpg")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and logo
pygame.display.set_caption("Udhaya space game")
icon = pygame.image.load('ico.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(3)
    enemyy_change.append(40)


# bullet
# ready=can't see the bullet
# fire=see the bullet

bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('digifont.ttf',32)
textx = 10
texty = 10

#gAME OVER TEXT
over_font = pygame.font.Font('digifont.ttf', 64)

def show_score(x, y):
    score = font.render("score: " + str(score_value),True, (0, 255,0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (250, 250))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# gameloop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystrokes are pressed oor not by right or  left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -2
            if event.key == pygame.K_RIGHT:
                playerx_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # spaceship movement
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement
    for i in range(num_of_enemies):

        #gameover
        if enemyy[i] > 420:
            for j in range(num_of_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 1
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullet_sound = mixer.Sound("explosion.wav")
            bullet_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change


    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
