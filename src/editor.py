import pygame, sys, anim, world
from pygame.locals import *

BOXSIZE = 48
BOARDWIDTH = 768
BOARDHEIGHT = 576
BRIGHTYELLOW = (255, 255, 0)

def leftTopCoordsOfBox (boxx, boxy):
    left = boxx * BOXSIZE
    top = boxy * BOXSIZE
    return (left, top)

def getBoxAtPixel(mousex, mousey):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(mousex, mousey):
                return (boxx, boxy)
    return (None, None)
    
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, BRIGHTYELLOW, (left - 2, top - 2, BOXSIZE + 4, BOXSIZE + 4), 4)
    
pygame.init()
pygame.display.set_caption('Map Editor')
DISPLAYSURF = pygame.display.set_mode((960, 800))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
x, y, z = 1, 1, 1
mousex, mousey, mouseClicked = 0, 0, False

while True:
    DISPLAYSURF.fill((255, 250, 205))
    world.loadOverworld(DISPLAYSURF, x, y, z)
    if z == 1: 
        worldname = "Overworld"
        anim.displayTerrain(DISPLAYSURF, 'A', 17, 1)
        anim.displayTerrain(DISPLAYSURF, 'B', 18, 1)
        anim.displayTerrain(DISPLAYSURF, 'C', 17, 2)
        anim.displayTerrain(DISPLAYSURF, 'D', 18, 2)
        anim.displayTerrain(DISPLAYSURF, 'E', 17, 3)
        anim.displayTerrain(DISPLAYSURF, 'F', 18, 3)
        anim.displayTerrain(DISPLAYSURF, 'G', 17, 4)
        anim.displayFeature(DISPLAYSURF, 'FA', 17, 6)
        anim.displayFeature(DISPLAYSURF, 'FF', 18, 6)
        anim.displayFeature(DISPLAYSURF, 'FG', 17, 7)
        anim.displayFeature(DISPLAYSURF, 'FH', 18, 7)
    else:
        worldname = "Dungeon %d" % z    
        anim.displayTerrain(DISPLAYSURF, 'H', 17, 1)
        anim.displayTerrain(DISPLAYSURF, 'I', 18, 1)
        anim.displayTerrain(DISPLAYSURF, 'J', 17, 2)
        anim.displayTerrain(DISPLAYSURF, 'K', 18, 2)
        anim.displayTerrain(DISPLAYSURF, 'L', 17, 3)
        anim.displayTerrain(DISPLAYSURF, 'M', 18, 3)
        anim.displayTerrain(DISPLAYSURF, 'N', 17, 4)
        anim.displayTerrain(DISPLAYSURF, 'O', 18, 4)
        anim.displayFeature(DISPLAYSURF, 'FB', 17, 6)
        anim.displayFeature(DISPLAYSURF, 'FC', 18, 6)
        anim.displayFeature(DISPLAYSURF, 'FD', 17, 7)
        anim.displayFeature(DISPLAYSURF, 'FE', 18, 7)
    textSurf = BASICFONT.render("%s -- Grid %d,%d" % (worldname, x, y), True, (0, 0, 0))
    textRect = textSurf.get_rect()
    textRect.topleft = (50, 576)
    #DISPLAYSURF.blit(textSurf, textRect)
    #pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (16, 600, 192, 144), 2)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (48, 624, 48, 48), 0)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (96, 624, 48, 48), 0)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (144, 624, 48, 48), 0)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (48, 672, 48, 48), 0)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (48, 720, 48, 48), 0)
    world.tinyOverworld(DISPLAYSURF, 1, 1, 1, 2, 2)
    anim.displayTerrain(DISPLAYSURF, 'A', 2, 15)
    #anim.displayTerrain(DISPLAYSURF, 'B', 2, 14)
    anim.displayTerrain(DISPLAYSURF, 'A', 3, 15)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True
    boxx, boxy = getBoxAtPixel(mousex, mousey)
    if boxx != None and boxy != None:
        drawHighlightBox(boxx, boxy)
    pygame.display.update()
