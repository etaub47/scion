import pygame, sys
from pygame.locals import *

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
    1: (0, 15), 2: (5, 18), 3: (8, 16), 4: (37, 19), 5: (53, 16),
    # colortile, large tiles, gray brick wall, sand, cobblestone
    6: (59, 15), 7: (57, 15), 8: (52, 17), 9: (7, 15), 10: (9, 14),
    # poison swamp, lava, soft tile, blue tile
    11: (23, 19), 12: (52, 13), 13: (56, 16), 14: (29, 16)
    # animated water: 36, 19 - 39, 19, animated swamp 23, 19 - 24, 19
    # animated lava: 49, 13 - 52, 13
}

featureMap = {
    'stairs_down_1': (15, 15), 'stairs_up_1': (31, 15), 'stairs_down_2': (41, 15), 'stairs_up_2': (42, 15),
    'tree': (14, 18)
}

def displayImage (DISPLAYSURF, imageRef, direction, step, x, y):
    sprite = spriteMap[imageRef]
    if step == 3: step = 1
    x_offset = (sprite[1][direction][0] + step) * 48
    y_offset = (sprite[1][direction][1]) * 48
    DISPLAYSURF.blit(sprite[0], (x, y), area=(x_offset, y_offset, 48, 48))

def displayTerrain (DISPLAYSURF, terrainRef, x, y):
    x_offset = (terrainMap[terrainRef][0]) * 48
    y_offset = (terrainMap[terrainRef][1]) * 48
    DISPLAYSURF.blit(sprite1, (x * 48, y * 48), area=(x_offset, y_offset, 48, 48))

def displaySquare (DISPLAYSURF, px, py):
    DISPLAYSURF.blit(sprite1, (144, 0), area=(px * 48, py * 48, 48, 48))
