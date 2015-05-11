import pygame, sys, anim
from pygame.locals import *

pygame.init()

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

FPS = 25
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((768, 576))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption('Scion')

i, j = 24, 1
x, y, direction = 250, 250, DOWN
speed = 5
step = 0
ratio, anim_ratio = 0, 3
px, py = 0, 15
tx = 1

while True:
    DISPLAYSURF.fill((255, 255, 255))
    textSurf = BASICFONT.render("%s,%s" % (str(px), str(py)), True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.bottomleft = 250, 250
    for r in range(0, 16):
        for s in range(0, 12):
            anim.displayTerrain(DISPLAYSURF, tx, r, s)
    anim.displaySquare(DISPLAYSURF, px, py)
    DISPLAYSURF.blit(textSurf, textRect)
    if direction == DOWN: 
        y += speed
        if y >= 450: direction = RIGHT
    elif direction == RIGHT:
        x += speed
        if x >= 450: direction = UP
    elif direction == UP:
        y -= speed
        if y <= 50: direction = LEFT
    elif direction == LEFT:
        x -= speed
        if x <= 50: direction = DOWN
    anim.displayImage(DISPLAYSURF, i, direction, step, x, y)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_o: i -= 1
            elif event.key == K_p: i += 1
            elif event.key == K_k: speed += 1
            elif event.key == K_m: speed -= 1
            elif event.key == K_LEFT: px -= 1
            elif event.key == K_RIGHT: px += 1
            elif event.key == K_UP: py -= 1
            elif event.key == K_DOWN: py += 1
            elif event.key == K_q: tx += 1
            elif event.key == K_a: tx -= 1
    pygame.display.update()
    fpsClock.tick(FPS)
    if ratio == anim_ratio: 
        step += 1
    else: 
        ratio += 1
    if step >= 4: step = 0
