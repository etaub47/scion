import pygame

from pygame.locals import *
from constants import *
from state import worldState, tempState, permState

sprite1 = pygame.image.load('../img/sprite1.png')
sprite2 = pygame.image.load('../img/sprite2.png')
sprite3 = pygame.image.load('../img/sprite3.png')
sprite4 = pygame.image.load('../img/sprite4.png')
sprite5 = pygame.image.load('../img/sprite5.png')
sprite6 = pygame.image.load('../img/sprite6.png')

imageMap = {
    'LIFE': (25, 0)
}

terrainMap = {
    # tx, ty, r, g, b, obstacleType (1=clear, 2=obstacle, 3=flight only)
    # nothing, grass
    '-': (0, 0, 255, 250, 205, TYPE_CLEAR), 'A': (0, 15, 0, 128, 0, TYPE_CLEAR), 
    # dungeon floor, brown brick wall
    'H': (5, 18, 105, 105, 105, TYPE_CLEAR), 'I': (8, 16, 139, 37, 0, TYPE_OBSTACLE_TALL), 
    # water, stones
    'B': (37, 19, 0, 238, 238, TYPE_WATER), 'C': (53, 16, 139, 90, 0, TYPE_OBSTACLE_TALL),
    # colortile, large tiles
    'J': (59, 15, 255, 250, 205, TYPE_CLEAR), 'K': (57, 15, 142, 142, 56, TYPE_CLEAR), 
    # gray brick wall, sand
    'L': (52, 17, 183, 183, 183, TYPE_OBSTACLE_TALL), 'D': (7, 15, 205, 179, 139, TYPE_CLEAR),
    # cobblestone, poison swamp
    'F': (9, 14, 139, 136, 120, TYPE_CLEAR), 'E': (23, 19, 118, 238, 0, TYPE_POISON), 
    # lava, soft tile
    'M': (52, 13, 238, 0, 0, TYPE_OBSTACLE), 'N': (56, 16, 125, 158, 192, TYPE_CLEAR), 
    # murky water, bridge
    'O': (19, 19, 56, 142, 142, TYPE_WATER), 'G': (43, 16, 139, 0, 0, TYPE_CLEAR),
    # animated water: 36, 19 - 39, 19, animated swamp 23, 19 - 24, 19, animated lava: 49, 13 - 52, 13
    'Q': (0, 46, 0, 0, 0, TYPE_CLEAR)
}

featureMap = {
    # tx, ty, obstacle type constant
    # stairs to dungeon, stairs to overworld, blue block
    'FA': (15, 15, TYPE_STAIRS), 'FB': (31, 15, TYPE_STAIRS), 'FC': (29, 16, TYPE_PUSHABLE), 
    # open door, closed door, tree
    'FD': (27, 11, TYPE_DOOR), 'FE': (23, 11, TYPE_DOOR), 'FF': (14, 18, TYPE_OBSTACLE_TALL),
    # statue, fountain, wings
    'FG': (28, 11, TYPE_PUSHABLE), 'FH': (63, 11, TYPE_OBSTACLE_TALL), 'IA': (15, 7, TYPE_ITEM), 
    # armor, book, shield
    'IB': (28, 21, TYPE_ITEM), 'IC': (58, 22, TYPE_ITEM), 'ID': (54, 22, TYPE_ITEM),
    # meat, gold, potion
    'IE': (36, 23, TYPE_ITEM), 'IF': (59, 23, TYPE_ITEM), 'IG': (63, 24, TYPE_ITEM), 
    # bracelet, staff, sword
    'IH': (60, 25, TYPE_ITEM), 'II': (4, 46, TYPE_ITEM), 'IJ': (43, 27, TYPE_ITEM),
    # chest, key, glove
    'IK': (43, 45, TYPE_ITEM), 'IL': (54, 45, TYPE_ITEM), 'IM': (13, 21, TYPE_ITEM),
    # boots, cloak, amulet
    'IN': (61, 20, TYPE_ITEM), 'IO': (5, 21, TYPE_ITEM), 'IP': (15, 20, TYPE_ITEM),
    # mirror, lantern, ring
    'IQ': (57, 45, TYPE_ITEM), 'IR': (14, 24, TYPE_ITEM), 'IS': (58, 25, TYPE_ITEM),
    # mini mirror, blast wall, mini fire, mini skull, question mark
    'AA': (3, 26, 6), 'AB': (2, 26, 6), 'AC': (23, 25, 6), 'AD': (42, 29, 6), 'AE': (36, 29, 6),
    # 1-5
    'AF': (11, 0, 7), 'AG': (12, 0, 7), 'AH': (13, 0, 7), 'AI': (14, 0, 7), 'AJ': (15, 0, 7)
}

class SpriteType:
    def __init__ (self, name, type, coords, size, crossReference):
        self.name, self.type, self.coords, self.size, self.crossReference = name, type, coords, size, crossReference

spriteMap = {
    'S1': SpriteType(sprite2, HERO, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'H1'),    # main hero
    'S2': SpriteType(sprite2, HERO, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'H2'),    # blonde girl
    'S3': SpriteType(sprite2, HERO, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'H3'),    # green-haired dude (unused)
    'S4': SpriteType(sprite2, HERO, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'H4'),    # blue-haired girl
    'S5': SpriteType(sprite2, HERO, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'H5'),    # long-haired caped dude
    'S6': SpriteType(sprite2, HERO, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'H6'),    # fancy girl
    'S7': SpriteType(sprite2, ENEMY, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'C7'),   # one-eyed creepy guy
    'S8': SpriteType(sprite2, HERO, [(9, 4), (9, 5), (9, 6), (9, 7)], BOXSIZE, 'H8'),    # wizened old man
    'S9': SpriteType(sprite3, ENEMY, [(0, 0), (9, 0), (3, 0), (6, 0)], BOXSIZE, 'C9'),   # ghost
    'S10': SpriteType(sprite3, ENEMY, [(0, 1), (9, 1), (3, 1), (6, 1)], BOXSIZE, 'C10'), # skeleton  
    'S11': SpriteType(sprite3, ENEMY, [(0, 2), (9, 2), (3, 2), (6, 2)], BOXSIZE, 'C11'), # goblin
    'S12': SpriteType(sprite3, ENEMY, [(0, 3), (9, 3), (3, 3), (6, 3)], BOXSIZE, 'C12'), # gargoyle
    'S13': SpriteType(sprite3, ENEMY, [(0, 4), (9, 4), (3, 4), (6, 4)], BOXSIZE, 'C13'), # water demon
    'S14': SpriteType(sprite3, ENEMY, [(0, 5), (9, 5), (3, 5), (6, 5)], BOXSIZE, 'C14'), # red-haired woman
    'S15': SpriteType(sprite3, ENEMY, [(0, 6), (9, 6), (3, 6), (6, 6)], BOXSIZE, 'C15'), # grim reaper
    'S16': SpriteType(sprite3, ENEMY, [(0, 7), (9, 7), (3, 7), (6, 7)], BOXSIZE, 'C16'), # blue powerful mage
    'S17': SpriteType(sprite4, HERO, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'H17'),  # simple girl
    'S18': SpriteType(sprite4, ENEMY, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'C18'), # hairy dude (unused)
    'S19': SpriteType(sprite4, ENEMY, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'C19'), # white-haired mage
    'S20': SpriteType(sprite4, ENEMY, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'C20'), # zombie
    'S21': SpriteType(sprite4, ENEMY, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'C21'), # worg
    'S22': SpriteType(sprite4, ENEMY, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'C22'), # chicken crow (unused)
    'S23': SpriteType(sprite4, ENEMY, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'C23'), # tan skeleton
    'S24': SpriteType(sprite6, ENEMY, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'C24'), # scorpion
    'S25': SpriteType(sprite5, ENEMY, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'C25'),
    'S26': SpriteType(sprite6, ENEMY, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'C26'),
    'S27': SpriteType(sprite5, ENEMY, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'C27'),
    'S28': SpriteType(sprite5, ENEMY, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'C28'),
    'S29': SpriteType(sprite6, ENEMY, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'C29'),
    'S30': SpriteType(sprite6, ENEMY, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'C30'), # bat
    'S31': SpriteType(sprite5, ENEMY, [(9, 4), (9, 5), (9, 6), (9, 7)], BOXSIZE, 'C31')
}

class Drawable:
    def getZIndex (self):  
        raise NotImplementedError("Please Implement this method")
    def draw (self, displaySurf): 
        raise NotImplementedError("Please Implement this method")

class Terrain (Drawable):
    def __init__ (self, wz, wx, wy, tx, ty, tkey):
        self.wz, self.wx, self.wy, self.tx, self.ty, self.tkey = wz, wx, wy, tx, ty, tkey
        self.addition = None
    def setAddition (self, addition):
        self.addition = addition
    def getZIndex (self):
        return self.ty * BOXSIZE
    def draw (self, displaySurf):
        if self.addition == "AA" and tempState.gotMirror and (tempState.timer / 5) % 2 == 0:
            displayTerrain(displaySurf, 'G', self.tx, self.ty)
        else:
            displayTerrain(displaySurf, self.tkey, self.tx, self.ty)

class Feature (Drawable):
    def __init__ (self, wz, wx, wy, tx, ty, tkey):
        self.wz, self.wx, self.wy, self.tx, self.ty, self.tkey = wz, wx, wy, tx, ty, tkey
    def getZIndex (self):  
        return self.ty * BOXSIZE
    def draw (self, displaySurf):
        displayFeature(displaySurf, self.tkey, self.tx, self.ty)

def getTerrainColor (terrainRef):
    return terrainMap[terrainRef][2:5]
    
def getTerrainObstacle (terrainRef):
    return terrainMap[terrainRef][5]

def getFeatureObstacle (featureRef):
    return featureMap[featureRef][2]
    
def getSpriteType (spriteRef):
    return spriteMap[spriteRef]

def displaySimpleImage (displaySurf, imageRef, x, y):
    image = imageMap[imageRef]
    x_offset, y_offset = image[0] * BOXSIZE, image[1] * BOXSIZE
    displaySurf.blit(sprite1, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
    
def displaySquare (displaySurf, px, py):
    displaySurf.blit(sprite1, (144, 0), area=(px * BOXSIZE, py * BOXSIZE, BOXSIZE, BOXSIZE))

def displayImage (displaySurf, spriteRef, direction, step, x, y):
    sprite = spriteMap[spriteRef]
    if step == 3: step = 1
    x_offset = (sprite.coords[direction][0] + step) * BOXSIZE
    y_offset = (sprite.coords[direction][1]) * BOXSIZE
    displaySurf.blit(sprite.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displaySprite (displaySurf, spriteRef, x, y):
    spriteType = spriteMap[spriteRef]
    x_offset = (spriteType.coords[DOWN][0]) * BOXSIZE
    y_offset = (spriteType.coords[DOWN][1]) * BOXSIZE
    displaySurf.blit(spriteType.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))                

def displayTerrain (displaySurf, terrainRef, tx, ty, offset_x = 0, offset_y = 0):
    if terrainRef in terrainMap:
        x_offset = (terrainMap[terrainRef][0]) * BOXSIZE
        y_offset = (terrainMap[terrainRef][1]) * BOXSIZE
        displaySurf.blit(sprite1, (tx * BOXSIZE + offset_x, ty * BOXSIZE + offset_y), 
            area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayFeature (displaySurf, featureRef, x, y, offset_x = 0, offset_y = 0):
    if featureRef[-1] == '\n': 
        featureRef = featureRef[:-1]
    x_offset = (featureMap[featureRef][0]) * BOXSIZE
    y_offset = (featureMap[featureRef][1]) * BOXSIZE
    displaySurf.blit(sprite1, (x * BOXSIZE + offset_x, y * BOXSIZE + offset_y), 
        area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def displayAddition (displaySurf, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    displaySurf.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def displayStairs (displaySurf):
    stairIcon = 'FA'
    if permState.wz > 0: stairIcon = 'FB'
    if tempState.stairs != None and tempState.stairs[2] == VISIBLE:
        displayFeature(displaySurf, stairIcon, tempState.stairs[0], tempState.stairs[1])

def displayLifeMeter (displaySurf):
    for heart in range(permState.life):
        displaySimpleImage(displaySurf, 'LIFE', heart * (BOXSIZE / 3) - (BOXSIZE / 2), 0)        

def drawHeadsUpDisplay (displaySurf):
    displayLifeMeter(displaySurf)

def redrawScreen (displaySurf):
    drawables = [permState.hero]
    drawables.extend(tempState.doors)
    drawables.extend(tempState.pushables)
    drawables.extend(tempState.creatures)
    drawables.extend(tempState.allies)
    drawables.extend(tempState.projectiles)
    drawables.extend(tempState.availableItems)
    for feature in worldState.getFeatures(permState.wz, permState.wx, permState.wy):
        if getFeatureObstacle(feature.tkey) == TYPE_OBSTACLE or getFeatureObstacle(feature.tkey) == TYPE_OBSTACLE_TALL:
            drawables.append(feature)
    for terrain in worldState.getTerrains(permState.wz, permState.wx, permState.wy):
        if getTerrainObstacle(terrain.tkey) == TYPE_OBSTACLE or getTerrainObstacle(terrain.tkey) == TYPE_OBSTACLE_TALL:
            drawables.append(terrain)
    for drawable in sorted(drawables, key = lambda drawable: drawable.getZIndex()):
        drawable.draw(displaySurf)
