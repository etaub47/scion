import pygame, graphics

from constants import *
from movables import *
from pygame import Rect
from state import worldState, tempState, permState
from items import AvailableItem, Door, Ally
from graphics import Feature

terrain = [[[[[0 for x in range(BOARDTILEHEIGHT)] for x in range(BOARDTILEWIDTH)]
    for x in range(WORLD_MAX_Y + 1)] for x in range(WORLD_MAX_X + 1)] for x in range(DUNGEON_MAX_Z + 1)]
loaded = [[[False for x in range(WORLD_MAX_Y + 1)] for x in range(WORLD_MAX_X + 1)] for x in range(DUNGEON_MAX_Z + 1)]
creatures, additions1, additions2, keyColors = [], [], [], {}
           
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
                        worldState.addTerrain(Terrain(wz, wx, wy, int(cx), int(cy), ckey))
            elif line[0] == '*':
                (tx, ty, tkey) = line[1:].split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                additions1.append((wz, wx, wy, int(tx), int(ty), tkey))
                worldState.getTerrain(wz, wx, wy, int(tx), int(ty)).setAddition(tkey)
            elif line[0] == '@':
                (tx, ty, tkey) = line[1:].split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                additions2.append((wz, wx, wy, int(tx), int(ty), tkey))
            else:
                (tx, ty, ttype, tkey) = line.split(",")
                if tkey[-1] == '\n': tkey = tkey[:-1]
                if int(ttype) == 1: worldState.addFeature(Feature(wz, wx, wy, int(tx), int(ty), tkey))
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
                terrainObstacle = graphics.getTerrainObstacle(terrain[wz][wx][wy][x][y])
                addition = getAddition1(wx, wy, wz, x, y)
                rect = Rect(x * BOXSIZE, y * BOXSIZE, BOXSIZE, BOXSIZE)
                rect2 = Rect(x * BOXSIZE, y * BOXSIZE + (BOXSIZE / 2) - 1, BOXSIZE, (BOXSIZE / 2) + 1)
                if terrainObstacle == TYPE_OBSTACLE:
                    if addition == "AA": tempState.fakeObstacles.append(rect) # mirror icon
                    else: tempState.obstacles.append(rect)
                elif terrainObstacle == TYPE_OBSTACLE_TALL:
                    if addition == "AA": tempState.fakeObstacles.append(rect2) # mirror icon
                    else: tempState.obstacles.append(rect2)
                elif terrainObstacle == TYPE_WATER: 
                    if addition == "AA": tempState.fakeWaterObstacles.append(rect) # mirror icon
                    else: tempState.waterObstacles.append(rect)
                elif terrainObstacle == TYPE_POISON: 
                    if addition == "AA": tempState.fakePoisonObstacles.append(rect) # mirror icon
                    else: tempState.poisonObstacles.append(rect)
                elif terrainObstacle == TYPE_CLEAR:
                    tempState.clearObstacles.append(rect)
        for feature in worldState.getFeatures(wz, wx, wy):
            featureObstacle = graphics.getFeatureObstacle(feature.tkey)
            x, y = feature.tx, feature.ty
            addition = getAddition1(wx, wy, wz, x, y)
            number = getAddition2(wx, wy, wz, x, y)
            # TODO: shrink these rectangles to allow people to walk behind trees?
            rect = Rect(x * BOXSIZE, y * BOXSIZE + (BOXSIZE / 2) - 1, BOXSIZE, (BOXSIZE / 2) + 1)
            if addition == "AD" and (wx, wy, wz, x, y) not in permState.unlockedDoors:
                showState = AFTER_VICTORY # skull
            elif addition == "AE" and (wx, wy, wz, x, y) not in permState.unlockedDoors:
                showState = AFTER_SECRET # question mark
            else:
                showState = VISIBLE # intentionally equivalent to OPEN for doors
            if featureObstacle == TYPE_OBSTACLE_TALL:
                if addition != "AA": # mirror
                    tempState.obstacles.append(rect)
            elif featureObstacle == TYPE_PUSHABLE:
                secretTrigger = getAddition1(wx, wy, wz, x, y) == "AE"
                tempState.pushables.append(Pushable(rect, feature.tkey, secretTrigger))
            elif featureObstacle == TYPE_ITEM:
                if (wx, wy, wz, x, y) not in permState.obtainedItems:
                    tempState.availableItems.append(AvailableItem(feature.tkey, x, y, showState))
            elif featureObstacle == TYPE_STAIRS:
                tempState.stairs = (x, y, showState, rect, number)
            elif featureObstacle == TYPE_DOOR:
                # a closed door without an addition is locked unless a key has been used
                if feature.tkey == 'FE' and (wx, wy, wz, x, y) not in permState.unlockedDoors and \
                        showState == OPEN:
                    showState = AFTER_KEY
                tempState.doors.append(Door(x, y, showState, number))
        for creature in getCreatures(wz, wx, wy):
            spriteRef, tx, ty = creature[5], creature[3], creature[4]
            spriteType = graphics.getSpriteType(spriteRef)
            if spriteType.type == ENEMY:
                tempState.creatures.append(Creature(spriteType.crossReference, tx, ty))
            else:
                tempState.allies.append(Ally(spriteRef, tx * BOXSIZE, ty * BOXSIZE))
                
def saveWorld (wx, wy, wz):
    if wz == 0: datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else: datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)
    with open(datafile, "w") as f:
        for cy in range(BOARDTILEHEIGHT):
            for cx in range(BOARDTILEWIDTH):
                f.write(terrain[wz][wx][wy][cx][cy])
            f.write('\n')
        for feature in worldState.getFeatures(wz, wx, wy):
            f.write("%d,%d,%d,%s\n" % (feature.tx, feature.ty, 1, feature.tkey))
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

def getAddition2 (wx, wy, wz, x, y):
    for addition in additions2:
        if addition[0] == wz and addition[1] == wx and addition[2] == wy and \
                addition[3] == x and addition[4] == y:
            return addition[5]
    return None

def drawTerrain (DISPLAYSURF, wx, wy, wz, offset_x = 0, offset_y = 0, real=False):
    for x in range(BOARDTILEWIDTH):
        for y in range(BOARDTILEHEIGHT):        
            addition = getAddition1(wx, wy, wz, x, y)
            if real and addition == "AA" and tempState.gotMirror and (tempState.timer / 5) % 2 == 0:
                graphics.displayTerrain(DISPLAYSURF, 'G', x, y, offset_x = offset_x, offset_y = offset_y)
            else:
                graphics.displayTerrain(DISPLAYSURF, terrain[wz][wx][wy][x][y], x, y, 
                    offset_x = offset_x, offset_y = offset_y)

def drawFeatures (DISPLAYSURF, wx, wy, wz, offset_x = 0, offset_y = 0, real=False):
    for feature in worldState.getFeatures(wz, wx, wy):
        if not real or graphics.getFeatureObstacle(feature.tkey) == TYPE_OBSTACLE or \
                graphics.getFeatureObstacle(feature.tkey) == TYPE_OBSTACLE_TALL:
            graphics.displayFeature(DISPLAYSURF, feature.tkey, feature.tx, feature.ty, 
                offset_x = offset_x, offset_y = offset_y)
                    
def drawMap (DISPLAYSURF, wx, wy, wz, offset_x = 0, offset_y = 0, real=False):
    drawTerrain(DISPLAYSURF, wx, wy, wz, offset_x, offset_y, False) # intentional
    drawFeatures(DISPLAYSURF, wx, wy, wz, offset_x, offset_y, real)

def drawEditorElements (DISPLAYSURF, wx, wy, wz, offset_x = 0, offset_y = 0):
    for creature in getCreatures(wz, wx, wy):
        graphics.displaySprite(DISPLAYSURF, creature[5], creature[3] * BOXSIZE + offset_x, 
            creature[4] * BOXSIZE + offset_y)
    for addition in additions1:
        if addition[0] == wz and addition[1] == wx and addition[2] == wy:
            graphics.displayFeature(DISPLAYSURF, addition[5], addition[3], addition[4])
    for addition in additions2:
        if addition[0] == wz and addition[1] == wx and addition[2] == wy:
            graphics.displayFeature(DISPLAYSURF, addition[5], addition[3], addition[4])
                
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
                            clr = graphics.getTerrainColor(ckey)
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

def addFeature (wz, wx, wy, x, y, type, value):
    if type == 1:
        worldState.removeFeature(wz, wx, wy, x, y)
        worldState.addFeature(Feature(wz, wx, wy, x, y, value))
    else:
        removeCreature(wz, wx, wy, x, y)
        creatures.append((wz, wx, wy, x, y, value))

def updateTerrain (wz, wx, wy, x, y, value):
    terrain[wz][wx][wy][x][y] = value

def addAddition (key, wz, wx, wy, x, y, value):
    if key == 1:
        removeAddition(1, wz, wx, wy, x, y)
        additions1.append((wz, wx, wy, x, y, value))
    else:
        removeAddition(2, wz, wx, wy, x, y)
        additions2.append((wz, wx, wy, x, y, value))    
    
def positionMatchesF (f, wz, wx, wy, x, y):
    return f.wz == wz and f.wx == wx and f.wy == wy and f.tx == x and f.ty == y

def positionMatches (c, wz, wx, wy, x, y):
    return c[0] == wz and c[1] == wx and c[2] == wy and c[3] == x and c[4] == y

def removeFeature (wz, wx, wy, x, y):
    worldState.removeFeature(wz, wx, wy, x, y)

def removeCreature (wz, wx, wy, x, y):
    creatures[:] = [c for c in creatures if not positionMatches(c, wz, wx, wy, x, y)]

def removeAddition (key, wz, wx, wy, x, y):
    if key == 1:
        additions1[:] = [a for a in additions1 if not positionMatches(a, wz, wx, wy, x, y)]
    else:
        additions2[:] = [a for a in additions2 if not positionMatches(a, wz, wx, wy, x, y)]

def getCreatures (wz, wx, wy):
    return [c for c in creatures if c[0] == wz and c[1] == wx and c[2] == wy]
