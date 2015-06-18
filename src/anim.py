import pygame, sys, time, world
from pygame.locals import *
from constants import *

sprite1 = pygame.image.load('../img/sprite1.png')
sprite2 = pygame.image.load('../img/sprite2.png')
sprite3 = pygame.image.load('../img/sprite3.png')
sprite4 = pygame.image.load('../img/sprite4.png')
sprite5 = pygame.image.load('../img/sprite5.png')
sprite6 = pygame.image.load('../img/sprite6.png')

spriteMap = { 
    'S1': (sprite2, [(0, 0), (0, 1), (0, 2), (0, 3)]), 'S2': (sprite2, [(3, 0), (3, 1), (3, 2), (3, 3)]),
    'S3': (sprite2, [(6, 0), (6, 1), (6, 2), (6, 3)]), 'S4': (sprite2, [(9, 0), (9, 1), (9, 2), (9, 3)]), 
    'S5': (sprite2, [(0, 4), (0, 5), (0, 6), (0, 7)]), 'S6': (sprite2, [(3, 4), (3, 5), (3, 6), (3, 7)]), 
    'S7': (sprite2, [(6, 4), (6, 5), (6, 6), (6, 7)]), 'S8': (sprite2, [(9, 4), (9, 5), (9, 6), (9, 7)]),
    'S9': (sprite3, [(0, 0), (9, 0), (3, 0), (6, 0)]), 'S10': (sprite3, [(0, 1), (9, 1), (3, 1), (6, 1)]),
    'S11': (sprite3, [(0, 2), (9, 2), (3, 2), (6, 2)]), 'S12': (sprite3, [(0, 3), (9, 3), (3, 3), (6, 3)]),
    'S13': (sprite3, [(0, 4), (9, 4), (3, 4), (6, 4)]), 'S14': (sprite3, [(0, 5), (9, 5), (3, 5), (6, 5)]),
    'S15': (sprite3, [(0, 6), (9, 6), (3, 6), (6, 6)]), 'S16': (sprite3, [(0, 7), (9, 7), (3, 7), (6, 7)]),
    'S17': (sprite4, [(0, 0), (0, 1), (0, 2), (0, 3)]), 'S18': (sprite4, [(3, 0), (3, 1), (3, 2), (3, 3)]),
    'S19': (sprite4, [(6, 0), (6, 1), (6, 2), (6, 3)]), 'S20': (sprite4, [(9, 0), (9, 1), (9, 2), (9, 3)]),
    'S21': (sprite4, [(0, 4), (0, 5), (0, 6), (0, 7)]), 'S22': (sprite4, [(3, 4), (3, 5), (3, 6), (3, 7)]),
    'S23': (sprite4, [(6, 4), (6, 5), (6, 6), (6, 7)]), 'S24': (sprite6, [(0, 0), (0, 1), (0, 2), (0, 3)]),
    'S25': (sprite5, [(3, 0), (3, 1), (3, 2), (3, 3)]), 'S26': (sprite6, [(6, 0), (6, 1), (6, 2), (6, 3)]),
    'S27': (sprite5, [(9, 0), (9, 1), (9, 2), (9, 3)]), 'S28': (sprite5, [(0, 4), (0, 5), (0, 6), (0, 7)]),
    'S29': (sprite6, [(3, 4), (3, 5), (3, 6), (3, 7)]), 'S30': (sprite6, [(6, 4), (6, 5), (6, 6), (6, 7)]),
    'S31': (sprite5, [(9, 4), (9, 5), (9, 6), (9, 7)])
}

terrainMap = {
    # nothing, grass
    '-': (0, 0, 255, 250, 205), 'A': (0, 15, 0, 128, 0), 
    # dungeon floor, brown brick wall, water, stones    
    'H': (5, 18, 105, 105, 105), 'I': (8, 16, 139, 37, 0), 'B': (37, 19, 0, 238, 238), 'C': (53, 16, 139, 90, 0),
    # colortile, large tiles, gray brick wall, sand
    'J': (59, 15, 255, 250, 205), 'K': (57, 15, 142, 142, 56), 'L': (52, 17, 183, 183, 183), 'D': (7, 15, 205, 179, 139),
    # cobblestone, poison swamp, lava, soft tile
    'F': (9, 14, 139, 136, 120), 'E': (23, 19, 118, 238, 0), 'M': (52, 13, 238, 0, 0), 'N': (56, 16, 125, 158, 192), 
    # murky water, bridge
    'O': (19, 19, 56, 142, 142), 'G': (43, 16, 139, 0, 0)
    # animated water: 36, 19 - 39, 19, animated swamp 23, 19 - 24, 19
    # animated lava: 49, 13 - 52, 13
}

featureMap = {
    # stairs to dungeon, stairs to overworld, blue tile, open door, closed door, tree
    'FA': (15, 15), 'FB': (31, 15), 'FC': (29, 16), 'FD': (27, 11), 'FE': (23, 11), 'FF': (14, 18),
    # statue, fountain, wings, armor, book, shield
    'FG': (28, 11), 'FH': (63, 11), 'IA': (15, 7), 'IB': (28, 21), 'IC': (58, 22), 'ID': (54, 22),
    # meat, gold, potion, bracelet, staff, sword
    'IE': (36, 23), 'IF': (59, 23), 'IG': (63, 24), 'IH': (60, 25), 'II': (4, 46), 'IJ': (43, 27),
    # chest, key, glove, boots, cloak, amulet
    'IK': (43, 45), 'IL': (54, 45), 'IM': (13, 21), 'IN': (61, 20), 'IO': (5, 21), 'IP': (15, 20),
    # mirror, lantern, ring
    'IQ': (57, 45), 'IR': (14, 24), 'IS': (58, 25),
    # mini mirror, blast wall, mini fire, mini skull, question mark
    'AA': (3, 26), 'AB': (2, 26), 'AC': (23, 25), 'AD': (42, 29), 'AE': (36, 29),
    # 1-5
    'AF': (11, 0), 'AG': (12, 0), 'AH': (13, 0), 'AI': (14, 0), 'AJ': (15, 0)
}

def getTerrainColor (terrainRef):
    return terrainMap[terrainRef][2:]

def displayImage (DISPLAYSURF, imageRef, direction, step, x, y):
    sprite = spriteMap[imageRef]
    if step == 3: step = 1
    x_offset = (sprite[1][direction][0] + step) * BOXSIZE
    y_offset = (sprite[1][direction][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite[0], (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayTerrain (DISPLAYSURF, terrainRef, x, y, offset_x = 0, offset_y = 0):
    if terrainRef in terrainMap:
        x_offset = (terrainMap[terrainRef][0]) * BOXSIZE
        y_offset = (terrainMap[terrainRef][1]) * BOXSIZE
        DISPLAYSURF.blit(sprite1, (x * BOXSIZE + offset_x, y * BOXSIZE + offset_y), 
            area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayFeature (DISPLAYSURF, featureRef, x, y, offset_x = 0, offset_y = 0):
    if featureRef[-1] == '\n': 
        featureRef = featureRef[:-1]
    x_offset = (featureMap[featureRef][0]) * BOXSIZE
    y_offset = (featureMap[featureRef][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x * BOXSIZE + offset_x, y * BOXSIZE + offset_y), 
        area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def displaySquare (DISPLAYSURF, px, py):
    DISPLAYSURF.blit(sprite1, (144, 0), area=(px * BOXSIZE, py * BOXSIZE, BOXSIZE, BOXSIZE))

def displayCreature (DISPLAYSURF, creatureRef, x, y, offset_x = 0, offset_y = 0):
    sprite = spriteMap[creatureRef]
    x_offset = (sprite[1][0][0]) * BOXSIZE
    y_offset = (sprite[1][0][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite[0], (x * BOXSIZE + offset_x, y * BOXSIZE + offset_y), 
        area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayAddition (DISPLAYSURF, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def scrollScreen (DISPLAYSURF, i, direction, step, x, y, wx, wy, wz):
    if direction == DOWN:
        for new_y in range(MAX_Y, MIN_Y, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y - MAX_Y - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy + 1, wz, offset_y = new_y, real=True)
            displayImage(DISPLAYSURF, i, direction, step, x, new_y)
            pygame.display.update()
    elif direction == RIGHT:
        for new_x in range(MAX_X, MIN_X, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x - MAX_X - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx + 1, wy, wz, offset_x = new_x, real=True)
            displayImage(DISPLAYSURF, i, direction, step, new_x, y)
            pygame.display.update()
    elif direction == UP:
        for new_y in range(MIN_Y, MAX_Y, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy - 1, wz, offset_y = new_y - MAX_Y, real=True)
            displayImage(DISPLAYSURF, i, direction, step, x, new_y)
            pygame.display.update()
    elif direction == LEFT:
        for new_x in range(MIN_X, MAX_X, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx - 1, wy, wz, offset_x = new_x - MAX_X, real=True)
            displayImage(DISPLAYSURF, i, direction, step, new_x, y)
            pygame.display.update()
