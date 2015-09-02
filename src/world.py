import pygame, anim

from constants import *
from movables import *
from pygame import Rect
from state import tempState, permState
from items import AvailableItem

terrain = [[[[[0 for x in range(BOARDTILEHEIGHT)] for x in range(BOARDTILEWIDTH)]
    for x in range(WORLD_MAX_Y + 1)] for x in range(WORLD_MAX_X + 1)] for x in range(DUNGEON_MAX_Z + 1)]
loaded = [[[False for x in range(WORLD_MAX_Y + 1)] for x in range(WORLD_MAX_X + 1)] for x in range(DUNGEON_MAX_Z + 1)]
features, creatures, additions1, additions2, keyColors = [], [], [], [], {}
           
def roomInRange (roomx, roomy, roomz):
    if roomx <= 0 or roomy <= 0: return False
    if roomz == 0:
        return roomx <= WORLD_MAX_X and roomy <= WORLD_MAX_Y
    else:
        return roomx <= DUNGEON_MAX_X and roomy <= DUNGEON_MAX_Y

def loadFile (wx, wy, wz):
    if wz == 0: datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else: datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)
    loaded[wz][wx][wy] = True
    with open(datafile, "r") as f:
        for cy, line in enumerate(f):
            if cy < BOARDTILEHEIGHT:
                for cx, ckey in enumerate(line):
                    if cx < BOARDTILEWIDTH:
                        terrain[wz][wx][wy][cx][cy] = ckey
            elif line[0] == '*':
                (tx, ty, tkey) = line[1:].split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                additions1.append((wz, wx, wy, int(tx), int(ty), tkey))
            elif line[0] == '@':
                (tx, ty, tkey) = line[1:].split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                additions2.append((wz, wx, wy, int(tx), int(ty), tkey))
            else:
                (tx, ty, ttype, tkey) = line.split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                if int(ttype) == 1: features.append((wz, wx, wy, int(tx), int(ty), tkey))
                elif int(ttype) == 2: creatures.append((wz, wx, wy, int(tx), int(ty), tkey))

def loadWorld (wx, wy, wz, real = False):
    for roomx in range(wx - 1, wx + 2):
        for roomy in range(wy - 1, wy + 2):
            if roomInRange(roomx, roomy, wz) and loaded[wz][roomx][roomy] == False:
                loadFile(roomx, roomy, wz)
    if real:
        tempState.clear()
        for x in range(BOARDTILEWIDTH):
            for y in range(BOARDTILEHEIGHT):
                terrainObstacle = anim.getTerrainObstacle(terrain[wz][wx][wy][x][y])
                rect = Rect(x * BOXSIZE, y * BOXSIZE, BOXSIZE, BOXSIZE)
                if terrainObstacle == TYPE_OBSTACLE: 
                    tempState.obstacles.append(rect)
                elif terrainObstacle == TYPE_LOW: 
                    tempState.lowObstacles.append(rect)
        for feature in features:
            if feature[0] == wz and feature[1] == wx and feature[2] == wy:
                featureObstacle = anim.getFeatureObstacle(feature[5])
                rect = Rect(feature[3] * BOXSIZE, feature[4] * BOXSIZE, BOXSIZE, BOXSIZE)
                if featureObstacle == TYPE_OBSTACLE:
                    tempState.obstacles.append(rect)
                elif featureObstacle == TYPE_PUSHABLE:
                    tempState.pushables.append(Pushable(rect, feature[5]))
                elif featureObstacle == TYPE_ITEM:
                    shown = getAddition1(wx, wy, wz, feature[3], feature[4]) != "AD"
                    tempState.availableItems.append(AvailableItem(feature[5], feature[3], feature[4], shown))
        for creature in getCreatures(wz, wx, wy):
            anim.createCreature(creature[5], creature[3], creature[4])
                
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
                f.write("%d,%d,%d,%s\n" % (feature[3], feature[4], 1, feature[5]))
        for creature in creatures:
            if creature[0] == wz and creature[1] == wx and creature[2] == wy:
                f.write("%d,%d,%d,%s\n" % (creature[3], creature[4], 2, creature[5]))
        for addition in additions1:
            if addition[0] == wz and addition[1] == wx and addition[2] == wy:
                f.write("*%d,%d,%s\n" % (addition[3], addition[4], addition[5]))
        for addition in additions2:
            if addition[0] == wz and addition[1] == wx and addition[2] == wy:
                f.write("@%d,%d,%s\n" % (addition[3], addition[4], addition[5]))

def getAddition1 (wx, wy, wz, x, y):
    for addition in additions1:
        if addition[0] == wz and addition[1] == wx and addition[2] == wy and \
                addition[3] == x and addition[4] == y:
            return addition[5]
    return None

def drawWorld (DISPLAYSURF, wx, wy, wz, offset_x = 0, offset_y = 0, real = False):
    for x in range(BOARDTILEWIDTH):
        for y in range(BOARDTILEHEIGHT):
            anim.displayTerrain(DISPLAYSURF, terrain[wz][wx][wy][x][y], x, y, 
                offset_x = offset_x, offset_y = offset_y)
    for feature in features:
        if feature[0] == wz and feature[1] == wx and feature[2] == wy:
            if not real or anim.getFeatureObstacle(feature[5]) == TYPE_OBSTACLE:
                anim.displayFeature(DISPLAYSURF, feature[5], feature[3], feature[4], 
                    offset_x = offset_x, offset_y = offset_y)
    if not real:
        for creature in getCreatures(wz, wx, wy):
            anim.displaySprite(DISPLAYSURF, creature[5], creature[3] * BOXSIZE + offset_x, 
                creature[4] * BOXSIZE + offset_y)
        for addition in additions1:
            if addition[0] == wz and addition[1] == wx and addition[2] == wy:
                anim.displayFeature(DISPLAYSURF, addition[5], addition[3], addition[4])
        for addition in additions2:
            if addition[0] == wz and addition[1] == wx and addition[2] == wy:
                anim.displayFeature(DISPLAYSURF, addition[5], addition[3], addition[4])
                
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
    if type == 1:
        removeFeature(wz, wx, wy, x, y)
        features.append((wz, wx, wy, x, y, value))
    else:
        removeCreature(wz, wx, wy, x, y)
        creatures.append((wz, wx, wy, x, y, value))

def addAddition (key, wz, wx, wy, x, y, value):
    if key == 1:
        removeAddition(1, wz, wx, wy, x, y)
        additions1.append((wz, wx, wy, x, y, value))
    else:
        removeAddition(2, wz, wx, wy, x, y)
        additions2.append((wz, wx, wy, x, y, value))    
    
def positionMatches (f, wz, wx, wy, x, y):
    return f[0] == wz and f[1] == wx and f[2] == wy and f[3] == x and f[4] == y

def removeFeature (wz, wx, wy, x, y):
    features[:] = [f for f in features if not positionMatches(f, wz, wx, wy, x, y)]

def removeCreature (wz, wx, wy, x, y):
    creatures[:] = [c for c in creatures if not positionMatches(c, wz, wx, wy, x, y)]

def removeAddition (key, wz, wx, wy, x, y):
    if key == 1:
        additions1[:] = [a for a in additions1 if not positionMatches(a, wz, wx, wy, x, y)]
    else:
        additions2[:] = [a for a in additions2 if not positionMatches(a, wz, wx, wy, x, y)]
        
def getCreatures (wz, wx, wy):
    return [c for c in creatures if c[0] == wz and c[1] == wx and c[2] == wy]
