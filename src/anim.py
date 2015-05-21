import pygame, sys
from pygame.locals import *
from constants import *

sprite1 = pygame.image.load('../img/sprite1.png')
sprite2 = pygame.image.load('../img/sprite2.png')
sprite3 = pygame.image.load('../img/sprite3.png')
sprite4 = pygame.image.load('../img/sprite4.png')
sprite5 = pygame.image.load('../img/sprite5.png')
sprite6 = pygame.image.load('../img/sprite6.png')

spriteMap = { 
    1: (sprite2, [(0, 0), (0, 1), (0, 2), (0, 3)]), 2: (sprite2, [(3, 0), (3, 1), (3, 2), (3, 3)]),
    3: (sprite2, [(6, 0), (6, 1), (6, 2), (6, 3)]), 4: (sprite2, [(9, 0), (9, 1), (9, 2), (9, 3)]), 
    5: (sprite2, [(0, 4), (0, 5), (0, 6), (0, 7)]), 6: (sprite2, [(3, 4), (3, 5), (3, 6), (3, 7)]), 
    7: (sprite2, [(6, 4), (6, 5), (6, 6), (6, 7)]), 8: (sprite2, [(9, 4), (9, 5), (9, 6), (9, 7)]),
    9: (sprite3, [(0, 0), (9, 0), (3, 0), (6, 0)]), 10: (sprite3, [(0, 1), (9, 1), (3, 1), (6, 1)]),
    11: (sprite3, [(0, 2), (9, 2), (3, 2), (6, 2)]), 12: (sprite3, [(0, 3), (9, 3), (3, 3), (6, 3)]),
    13: (sprite3, [(0, 4), (9, 4), (3, 4), (6, 4)]), 14: (sprite3, [(0, 5), (9, 5), (3, 5), (6, 5)]),
    15: (sprite3, [(0, 6), (9, 6), (3, 6), (6, 6)]), 16: (sprite3, [(0, 7), (9, 7), (3, 7), (6, 7)]),
    17: (sprite4, [(0, 0), (0, 1), (0, 2), (0, 3)]), 18: (sprite4, [(3, 0), (3, 1), (3, 2), (3, 3)]),
    19: (sprite4, [(6, 0), (6, 1), (6, 2), (6, 3)]), 20: (sprite4, [(9, 0), (9, 1), (9, 2), (9, 3)]),
    21: (sprite4, [(0, 4), (0, 5), (0, 6), (0, 7)]), 22: (sprite4, [(3, 4), (3, 5), (3, 6), (3, 7)]),
    23: (sprite4, [(6, 4), (6, 5), (6, 6), (6, 7)]), 24: (sprite6, [(0, 0), (0, 1), (0, 2), (0, 3)]),
    25: (sprite5, [(3, 0), (3, 1), (3, 2), (3, 3)]), 26: (sprite6, [(6, 0), (6, 1), (6, 2), (6, 3)]),
    27: (sprite5, [(9, 0), (9, 1), (9, 2), (9, 3)]), 28: (sprite5, [(0, 4), (0, 5), (0, 6), (0, 7)]),
    29: (sprite6, [(3, 4), (3, 5), (3, 6), (3, 7)]), 30: (sprite6, [(6, 4), (6, 5), (6, 6), (6, 7)]),
    31: (sprite5, [(9, 4), (9, 5), (9, 6), (9, 7)])
}

terrainMap = {
    # grass, dungeon floor, brown brick wall, water, stones
    'A': (0, 15), 'H': (5, 18), 'I': (8, 16), 'B': (37, 19), 'C': (53, 16),
    # colortile, large tiles, gray brick wall, sand, cobblestone
    'J': (59, 15), 'K': (57, 15), 'L': (52, 17), 'D': (7, 15), 'F': (9, 14),
    # poison swamp, lava, soft tile, blue tile, bridge
    'E': (23, 19), 'M': (52, 13), 'N': (56, 16), 'O': (29, 16), 'G': (43, 16)
    # animated water: 36, 19 - 39, 19, animated swamp 23, 19 - 24, 19
    # animated lava: 49, 13 - 52, 13
}

featureMap = {
    # stairs to dungeon, stairs to overworld, , , , tree
    'FA': (15, 15), 'FB': (31, 15), 'FC': (41, 15), 'FD': (42, 15), 'FE': (23, 11), 'FF': (14, 18),
    # statue, fountain
    'FG': (28, 11), 'FH': (63, 11)
}

def displayImage (DISPLAYSURF, imageRef, direction, step, x, y):
    sprite = spriteMap[imageRef]
    if step == 3: step = 1
    x_offset = (sprite[1][direction][0] + step) * BOXSIZE
    y_offset = (sprite[1][direction][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite[0], (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayTerrain (DISPLAYSURF, terrainRef, x, y):
    if terrainRef in terrainMap:
        x_offset = (terrainMap[terrainRef][0]) * BOXSIZE
        y_offset = (terrainMap[terrainRef][1]) * BOXSIZE
        DISPLAYSURF.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayFeature (DISPLAYSURF, featureRef, x, y):
    if featureRef[-1] == '\n': 
        featureRef = featureRef[:-1]
    x_offset = (featureMap[featureRef][0]) * BOXSIZE
    y_offset = (featureMap[featureRef][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def displaySquare (DISPLAYSURF, px, py):
    DISPLAYSURF.blit(sprite1, (144, 0), area=(px * BOXSIZE, py * BOXSIZE, BOXSIZE, BOXSIZE))

def displayCreature (DISPLAYSURF, creatureRef, x, y):
    sprite = spriteMap[creatureRef]
    x_offset = (sprite[1][0][0]) * BOXSIZE
    y_offset = (sprite[1][0][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite[0], (x * BOXSIZE, y * BOXSIZE), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
