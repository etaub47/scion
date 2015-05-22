import pygame, anim
from constants import *

terrain = [[[[[0 for x in range(BOARDTILEHEIGHT)] for x in range(BOARDTILEWIDTH)] 
    for x in range(4)] for x in range(4)] for x in range(5)]
features = []
colors = { '-': OFFWHITE, 'A': (0, 128, 0), 'B': (0, 238, 238), 'C': (139, 90, 0), 'D': (205, 179, 139),
           'E': (118, 238, 0), 'F': (139, 136, 120), 'G': (139, 0, 0) }
           
def roomInRange (roomx, roomy):
    return roomx > 0 and roomy > 0 and roomx <= WORLD_MAX_X and roomy <= WORLD_MAX_Y

def loadFile (wx, wy, wz):
    if wz == 0: datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else: datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)    
    with open(datafile, "r") as f:
        for cy, line in enumerate(f):
            if cy < BOARDTILEHEIGHT:
                for cx, ckey in enumerate(line):
                    if cx < BOARDTILEWIDTH:
                        terrain[wz][wx][wy][cx][cy] = ckey
            else:
                (tx, ty, ttype, tkey) = line.split(",")
                features.append((wz, wx, wy, int(tx), int(ty), ttype, tkey))

def loadWorld (wx, wy, wz):
    for roomx in range(wx - 1, wx + 2):
        for roomy in range(wy - 1, wy + 2):
            if roomInRange(roomx, roomy):
                loadFile(roomx, roomy, wz)
                
def drawWorld (DISPLAYSURF, wx, wy, wz):
    for x in range(BOARDTILEWIDTH):
        for y in range(BOARDTILEHEIGHT):
            anim.displayTerrain(DISPLAYSURF, terrain[wz][wx][wy][x][y], x, y)
    for feature in features:
        if feature[0] == wz and feature[1] == wx and feature[2] == wy:
            if feature[5] == 1:
                anim.displayFeature(DISPLAYSURF, feature[6], feature[3], feature[4])
            elif feature[5] == 2:
                anim.displayCreature(DISPLAYSURF, feature[6], feature[3], feature[4])

def tinyOverworld (DISPLAYSURF, wx, wy, wz):
    for gx in range(3):
        for gy in range(3):
            roomx, roomy = wx - 1 + gx, wy - 1 + gy
            if roomInRange(roomx, roomy):
                for x in range(BOARDTILEWIDTH):
                    for y in range(BOARDTILEHEIGHT):
                        ckey = terrain[wz][roomx][roomy][x][y]
                        clr = colors[ckey]
                        rect_x = BOXSIZE * (gx + 1) + (x * 3)
                        rect_y = BOARDHEIGHT + (BOXSIZE * (gy + 1)) + (y * 4)
                        pygame.draw.rect(DISPLAYSURF, clr, (rect_x, rect_y, 3, 4), 0)
            else:
                rect_x = BOXSIZE * (gx + 1)
                rect_y = BOARDHEIGHT + (BOXSIZE * (gy + 1))
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (rect_x, rect_y, BOXSIZE, BOXSIZE), 0)
    pygame.draw.rect(DISPLAYSURF, WHITE, (BOXSIZE * 2 - 2, 
        BOXSIZE * (BOARDTILEHEIGHT + 2) - 2, BOXSIZE + 4, BOXSIZE + 4), 4)

def updateTerrain (wz, wx, wy, x, y, value):
    terrain[wz][wx][wy][x][y] = value

def addFeature (wz, wx, wy, x, y, type, value):
    features.append((wz, wx, wy, x, y, type, value))
