import pygame, sys, anim, world
from pygame.locals import *
from constants import *

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
    
def drawHighlightBox(boxx, boxy, clr=BRIGHTYELLOW):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, clr, (left - 2, top - 2, BOXSIZE + 4, BOXSIZE + 4), 4)
    
pygame.init()
pygame.display.set_caption('Map Editor')
DISPLAYSURF = pygame.display.set_mode((960, 800))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
x, y, z = 1, 1, 0
mousex, mousey, mouseDown = 0, 0, False
selection = None

world.loadWorld(x, y, z)

buttons1=[(0, 'A', 17, 1), (0, 'B', 18, 1), (0, 'C', 17, 2), (0, 'D', 18, 2), (0, 'E', 17, 3),
          (0, 'F', 18, 3), (0, 'G', 17, 4), (1, 'FA', 17, 6), (1, 'FF', 18, 6), (1, 'FG', 17, 7),
          (1, 'FH', 18, 7), (2, 11, 5, 13), (2, 13, 5, 14), (2, 14, 5, 15), (2, 16, 6, 13),
          (2, 19, 6, 14), (2, 21, 6, 15), (2, 23, 7, 13), (2, 24, 7, 14), (2, 29, 7, 15)]
buttons2=[(0, 'H', 17, 1), (0, 'I', 18, 1), (0, 'K', 17, 2), (0, 'L', 18, 2), (0, 'M', 17, 3),
          (0, 'N', 18, 3), (0, 'O', 17, 4), (1, 'FB', 17, 6), (1, 'FC', 18, 6), (1, 'FD', 17, 7),
          (1, 'FE', 18, 7), (2, 9, 5, 13), (2, 10, 5, 14), (2, 12, 5, 15), (2, 15, 6, 13),
          (2, 20, 6, 14), (2, 26, 6, 15), (2, 27, 7, 13), (2, 28, 7, 14), (2, 30, 7, 15)]

def getButtons (z):
    if z == 0: return buttons1
    else: return buttons2

while True:
    DISPLAYSURF.fill(GRAY)
    world.drawWorld(DISPLAYSURF, x, y, z)
    for button in getButtons(z):
        if button[0] == 0: anim.displayTerrain(DISPLAYSURF, button[1], button[2], button[3])
        elif button[0] == 1: anim.displayFeature(DISPLAYSURF, button[1], button[2], button[3])
        elif button[0] == 2: anim.displayCreature(DISPLAYSURF, button[1], button[2], button[3])
    #textSurf = BASICFONT.render("%s -- Grid %d,%d" % (worldname, x, y), True, (0, 0, 0))
    #textRect = textSurf.get_rect()
    #textRect.topleft = (50, 576)
    #DISPLAYSURF.blit(textSurf, textRect)
    world.tinyOverworld(DISPLAYSURF, x, y, z)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if mouseDown and boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT:
                if selection != None and selection[0] == 0:
                    world.updateTerrain(z, x, y, boxx, boxy, selection[1])
                elif selection != None and selection[0] > 0:
                    world.addFeature(z, x, y, boxx, boxy, selection[0], selection[1])                
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            mouseDown = True
            if selection != None and selection[0] == 0 and boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT:
                world.updateTerrain(z, x, y, boxx, boxy, selection[1])
            for button in getButtons(z):
                if boxx == button[2] and boxy == button[3]:
                    selection = button
        elif event.type == MOUSEBUTTONUP:
            mouseDown = False
        elif event.type == KEYDOWN and event.key == K_s:
            world.saveWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_RIGHT and world.roomInRange(x + 1, y):
            world.saveWorld(x, y, z)
            x += 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_LEFT and world.roomInRange(x - 1, y):
            world.saveWorld(x, y, z)
            x -= 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_DOWN and world.roomInRange(x, y + 1):
            world.saveWorld(x, y, z)
            y += 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_UP and world.roomInRange(x, y - 1):
            world.saveWorld(x, y, z)
            y -= 1
            world.loadWorld(x, y, z)
    if selection != None:
        drawHighlightBox(selection[2], selection[3], WHITE)
    if boxx != None and boxy != None and boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT:
        drawHighlightBox(boxx, boxy)
    for button in getButtons(z):
        if boxx == button[2] and boxy == button[3]:
            drawHighlightBox(boxx, boxy)
    pygame.display.update()
