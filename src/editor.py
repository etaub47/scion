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
boxx, boxy = None, None
selection = None
world.loadWorld(x, y, z)

buttons1=[(0, 'A', 17, 1), (0, 'B', 18, 1), (0, 'C', 17, 2), (0, 'D', 18, 2), (0, 'E', 17, 3),
      (0, 'F', 18, 3), (0, 'G', 17, 4), (1, 'FA', 17, 6), (1, 'FF', 18, 6), (1, 'FG', 17, 7),
      (1, 'FH', 18, 7), (2, 'S11', 5, 13), (2, 'S13', 5, 14), (2, 'S14', 5, 15), (2, 'S16', 6, 13),
      (2, 'S19', 6, 14), (2, 'S21', 6, 15), (2, 'S23', 7, 13), (2, 'S24', 7, 14), (2, 'S29', 7, 15),
      (1, 'IA', 17, 9), (1, 'IN', 18, 9), (1, 'IM', 17, 10), (1, 'ID', 18, 10), (1, 'IE', 17, 11),
      (1, 'IF', 18, 11), (1, 'IG', 17, 12), (1, 'IH', 18, 12), (1, 'II', 17, 13), (1, 'IO', 18, 13),
      (1, 'IK', 17, 14), (1, 'IL', 18, 14), (1, 'IP', 17, 15), (1, 'IQ', 18, 15), 
      (1, 'IJ', 9, 13), (1, 'IB', 10, 13), (1, 'IC', 11, 13), (1, 'IR', 12, 13), (1, 'IS', 13, 13),
      (3, 'AA', 9, 14), (3, 'AB', 10, 14), (3, 'AC', 11, 14), (3, 'AD', 12, 14), (3, 'AE', 13, 14),
      (4, 'AF', 9, 15), (4, 'AG', 10, 15), (4, 'AH', 11, 15), (4, 'AI', 12, 15), (4, 'AJ', 13, 15),
      (2, 'S2', 14, 13), (2, 'S17', 15, 13), (2, 'S4', 14, 14), (2, 'S5', 15, 14), (2, 'S6', 14, 15),
      (2, 'S8', 15, 15)]
buttons2=[(0, 'H', 17, 1), (0, 'I', 18, 1), (0, 'K', 17, 2), (0, 'L', 18, 2), (0, 'M', 17, 3),
      (0, 'N', 18, 3), (0, 'O', 17, 4), (1, 'FB', 17, 6), (1, 'FC', 18, 6), (1, 'FD', 17, 7),
      (1, 'FE', 18, 7), (2, 'S9', 5, 13), (2, 'S10', 5, 14), (2, 'S12', 5, 15), (2, 'S15', 6, 13),
      (2, 'S20', 6, 14), (2, 'S26', 6, 15), (2, 'S27', 7, 13), (2, 'S28', 7, 14), (2, 'S30', 7, 15),
      (1, 'IA', 17, 9), (1, 'IN', 18, 9), (1, 'IM', 17, 10), (1, 'ID', 18, 10), (1, 'IE', 17, 11),
      (1, 'IF', 18, 11), (1, 'IG', 17, 12), (1, 'IH', 18, 12), (1, 'II', 17, 13), (1, 'IO', 18, 13),
      (1, 'IK', 17, 14), (1, 'IL', 18, 14), (1, 'IP', 17, 15), (1, 'IQ', 18, 15),
      (1, 'IJ', 9, 13), (1, 'IB', 10, 13), (1, 'IC', 11, 13), (1, 'IR', 12, 13), (1, 'IS', 13, 13),
      (3, 'AA', 9, 14), (3, 'AB', 10, 14), (3, 'AC', 11, 14), (3, 'AD', 12, 14), (3, 'AE', 13, 14),
      (4, 'AF', 9, 15), (4, 'AG', 10, 15), (4, 'AH', 11, 15), (4, 'AI', 12, 15), (4, 'AJ', 13, 15),
      (2, 'S2', 14, 13), (2, 'S17', 15, 13), (2, 'S4', 14, 14), (2, 'S5', 15, 14), (2, 'S6', 14, 15),
      (2, 'S8', 15, 15)]

def getButtons (z):
    if z == 0: return buttons1
    else: return buttons2

while True:
    DISPLAYSURF.fill(GRAY)
    world.drawWorld(DISPLAYSURF, x, y, z)
    for button in getButtons(z):
        if button[0] == 0: anim.displayTerrain(DISPLAYSURF, button[1], button[2], button[3])
        elif button[0] == 2: anim.displayCreature(DISPLAYSURF, button[1], button[2] * BOXSIZE, button[3] * BOXSIZE)
        elif button[0] == 1 or button[0] == 3 or button[0] == 4:
            anim.displayFeature(DISPLAYSURF, button[1], button[2], button[3])
    if z == 0: worldname = 'Overworld'
    else: worldname = 'Dungeon %d' % z        
    textSurf = BASICFONT.render("%s -- (%d,%d)" % (worldname, x, y), True, WHITE)
    textRect = textSurf.get_rect()
    textRect.topleft = (300, 576)
    DISPLAYSURF.blit(textSurf, textRect)
    world.tinyOverworld(DISPLAYSURF, x, y, z)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            if mouseDown and boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT and selection != None:
                if selection[0] == 0:
                    world.updateTerrain(z, x, y, boxx, boxy, selection[1])
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            mouseDown = True
            if boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT and selection != None:
                if selection[0] == 0:
                    world.updateTerrain(z, x, y, boxx, boxy, selection[1])
                elif selection[0] == 3:
                    world.addAddition(1, z, x, y, boxx, boxy, selection[1])
                elif selection[0] == 4:
                    world.addAddition(2, z, x, y, boxx, boxy, selection[1])
                else:
                    world.addFeature(z, x, y, boxx, boxy, selection[0], selection[1])
            for button in getButtons(z):
                if boxx == button[2] and boxy == button[3]:
                    selection = button
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            mouseDown = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            world.removeFeature(z, x, y, boxx, boxy)
            world.removeCreature(z, x, y, boxx, boxy)
            world.removeAddition(1, z, x, y, boxx, boxy)
            world.removeAddition(2, z, x, y, boxx, boxy)
        elif event.type == KEYDOWN and event.key == K_s:
            world.saveWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_RIGHT and world.roomInRange(x + 1, y, z):
            world.saveWorld(x, y, z)
            x += 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_LEFT and world.roomInRange(x - 1, y, z):
            world.saveWorld(x, y, z)
            x -= 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_DOWN and world.roomInRange(x, y + 1, z):
            world.saveWorld(x, y, z)
            y += 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and event.key == K_UP and world.roomInRange(x, y - 1, z):
            world.saveWorld(x, y, z)
            y -= 1
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and (event.key == K_PAGEDOWN or event.key == K_F9 or event.key == K_PERIOD):
            world.saveWorld(x, y, z)
            (x, y) = (1, 1)
            z += 1
            if z > DUNGEON_MAX_Z: z = 0
            world.loadWorld(x, y, z)
        elif event.type == KEYDOWN and (event.key == K_PAGEUP or event.key == K_F7 or event.key == K_COMMA):
            world.saveWorld(x, y, z)
            (x, y) = (1, 1)
            z -= 1
            if z < 0: z = DUNGEON_MAX_Z
            world.loadWorld(x, y, z)
    if selection != None:
        drawHighlightBox(selection[2], selection[3], WHITE)
    if boxx != None and boxy != None and boxx < BOARDTILEWIDTH and boxy < BOARDTILEHEIGHT:
        drawHighlightBox(boxx, boxy)
    for button in getButtons(z):
        if boxx == button[2] and boxy == button[3]:
            drawHighlightBox(boxx, boxy)
    pygame.display.update()
