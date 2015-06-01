import pygame, anim
from constants import *

terrain = [[[[[0 for x in range(BOARDTILEHEIGHT)] for x in range(BOARDTILEWIDTH)] 
    for x in range(WORLD_MAX_Y + 1)] for x in range(WORLD_MAX_X + 1)] for x in range(DUNGEON_MAX_Z + 1)]
features = []
keyColors = {}
           
def roomInRange (roomx, roomy, roomz):
    if roomz == 0:
        return roomx > 0 and roomy > 0 and roomx <= WORLD_MAX_X and roomy <= WORLD_MAX_Y
    else:
        return roomx > 0 and roomy > 0 and roomx <= DUNGEON_MAX_X and roomy <= DUNGEON_MAX_Y

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
                if tkey[-1] == '\n': tkey = tkey[:-1]
                features.append((wz, wx, wy, int(tx), int(ty), int(ttype), tkey))

def loadWorld (wx, wy, wz):
    features[:] = []
    for roomx in range(wx - 1, wx + 2):
        for roomy in range(wy - 1, wy + 2):
            if roomInRange(roomx, roomy, wz):
                loadFile(roomx, roomy, wz)
                
def saveWorld (wx, wy, wz):
    if wz == 0: datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else: datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)
    with open(datafile, "w") as f:
        for cy in range(BOARDTILEHEIGHT):
            for cx in range(BOARDTILEWIDTH):
                f.write(terrain[wz][wx][wy][cx][cy])
            f.write('\n')
        for feature in features:
            if feature[0] == wz and feature[1] == wx and feature[2] == wy:
                f.write("%d,%d,%d,%s\n" % (feature[3], feature[4], feature[5], feature[6]))
                
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
            if roomInRange(roomx, roomy, wz):
                for x in range(BOARDTILEWIDTH):
                    for y in range(BOARDTILEHEIGHT):
                        ckey = terrain[wz][roomx][roomy][x][y]
                        if ckey in keyColors:
                            clr = keyColors[ckey]
                        else:
                            clr = anim.getTerrainColor(ckey)
                            keyColors[ckey] = clr
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
    removeFeature(wz, wx, wy, x, y)
    features.append((wz, wx, wy, x, y, type, value))
    
def featureMatches (f, wz, wx, wy, x, y):
    return f[0] == wz and f[1] == wx and f[2] == wy and f[3] == x and f[4] == y

def removeFeature (wz, wx, wy, x, y):
    features[:] = [f for f in features if not featureMatches(f, wz, wx, wy, x, y)]
