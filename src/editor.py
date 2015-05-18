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

DISPLAYSURF = pygame.display.set_mode((960, 768))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF.fill((255, 255, 255))
x, y, z = 1, 1, 1
mousex, mousey, mouseClicked = 0, 0, False

while True:
    DISPLAYSURF.fill((255, 255, 255))
    world.loadOverworld(DISPLAYSURF, x, y, z)
    if z == 1: worldname = "Overworld"
    else: worldname = "Dungeon %d" % z    
    textSurf = BASICFONT.render("%s -- Grid %d,%d" % (worldname, x, y), True, (0, 0, 0))
    textRect = textSurf.get_rect()
    textRect.bottomleft = (768, 32)
    DISPLAYSURF.blit(textSurf, textRect)
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
    print boxx, boxy
    if boxx != None and boxy != None:
        drawHighlightBox(boxx, boxy)
    pygame.display.update()
