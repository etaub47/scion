import pygame, sys, time, world, random
from pygame.locals import *
from constants import *
from movables import *
from state import tempState, permState

imageMap = {
    'LIFE': (25, 0)
}

terrainMap = {
    # tx, ty, r, g, b, obstacleType (1=clear, 2=obstacle, 3=flight only)
    # nothing, grass
    '-': (0, 0, 255, 250, 205, TYPE_CLEAR), 'A': (0, 15, 0, 128, 0, TYPE_CLEAR), 
    # dungeon floor, brown brick wall
    'H': (5, 18, 105, 105, 105, TYPE_CLEAR), 'I': (8, 16, 139, 37, 0, TYPE_OBSTACLE), 
    # water, stones
    'B': (37, 19, 0, 238, 238, TYPE_WATER), 'C': (53, 16, 139, 90, 0, TYPE_OBSTACLE),
    # colortile, large tiles
    'J': (59, 15, 255, 250, 205, TYPE_CLEAR), 'K': (57, 15, 142, 142, 56, TYPE_CLEAR), 
    # gray brick wall, sand
    'L': (52, 17, 183, 183, 183, TYPE_OBSTACLE), 'D': (7, 15, 205, 179, 139, TYPE_CLEAR),
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
    # tx, ty, obstacleType (4=pushable, 5=item, 6=addition1, 7=addition2, 8=stairs)
    # stairs to dungeon, stairs to overworld, blue block
    'FA': (15, 15, TYPE_STAIRS), 'FB': (31, 15, TYPE_STAIRS), 'FC': (29, 16, TYPE_PUSHABLE), 
    # open door, closed door, tree
    'FD': (27, 11, TYPE_DOOR), 'FE': (23, 11, TYPE_DOOR), 'FF': (14, 18, TYPE_OBSTACLE),
    # statue, fountain, wings
    'FG': (28, 11, TYPE_PUSHABLE), 'FH': (63, 11, TYPE_OBSTACLE), 'IA': (15, 7, TYPE_ITEM), 
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

def getTerrainColor (terrainRef):
    return terrainMap[terrainRef][2:5]
    
def getTerrainObstacle (terrainRef):
    return terrainMap[terrainRef][5]

def getFeatureObstacle (featureRef):
    return featureMap[featureRef][2]

def displaySimpleImage (displaySurf, imageRef, x, y):
    image = imageMap[imageRef]
    x_offset, y_offset = image[0] * BOXSIZE, image[1] * BOXSIZE
    displaySurf.blit(sprite1, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
    
def displayLifeMeter (displaySurf, life):
    for heart in range(life):
        displaySimpleImage(displaySurf, 'LIFE', heart * (BOXSIZE / 3) - (BOXSIZE / 2), 0)        

def displayImage (displaySurf, spriteRef, direction, step, x, y):
    sprite = spriteMap[spriteRef]
    if step == 3: step = 1
    x_offset = (sprite.coords[direction][0] + step) * BOXSIZE
    y_offset = (sprite.coords[direction][1]) * BOXSIZE
    displaySurf.blit(sprite.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

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

def displayPushable (displaySurf, featureRef, x, y):
    if featureRef[-1] == '\n': 
        featureRef = featureRef[:-1]
    x_offset = (featureMap[featureRef][0]) * BOXSIZE
    y_offset = (featureMap[featureRef][1]) * BOXSIZE
    displaySurf.blit(sprite1, (x, y), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def displaySquare (displaySurf, px, py):
    displaySurf.blit(sprite1, (144, 0), area=(px * BOXSIZE, py * BOXSIZE, BOXSIZE, BOXSIZE))

def displayCreature (displaySurf, creature):
    frame = 1 if creature.step == 3 else creature.step
    spriteType = creature.creatureType.spriteType
    x_offset = (spriteType.coords[creature.direction][0] + frame) * BOXSIZE
    y_offset = (spriteType.coords[creature.direction][1]) * BOXSIZE
    displaySurf.blit(spriteType.name, (creature.x, creature.y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displaySprite (displaySurf, spriteRef, x, y):
    spriteType = spriteMap[spriteRef]
    x_offset = (spriteType.coords[DOWN][0]) * BOXSIZE
    y_offset = (spriteType.coords[DOWN][1]) * BOXSIZE
    displaySurf.blit(spriteType.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))                

def displayHero (displaySurf, hero):
    frame = 1 if hero.step == 3 else hero.step
    spriteType = hero.heroType.spriteType
    x_offset = (spriteType.coords[hero.direction][0] + frame) * BOXSIZE
    y_offset = (spriteType.coords[hero.direction][1]) * BOXSIZE
    displaySurf.blit(spriteType.name, (hero.x, hero.y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
    #pygame.draw.rect(displaySurf, BRIGHTYELLOW, hero.rect, 1)

def displayAddition (displaySurf, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    displaySurf.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def scrollScreen (displaySurf, hero, wx, wy, wz):
    if hero.direction == DOWN:
        for new_y in range(MAX_Y - BOXSIZE, MIN_Y, 0 - (BOXSIZE / 3)):
            world.drawWorld(displaySurf, wx, wy, wz, offset_y = new_y - MAX_Y - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(displaySurf, wx, wy + 1, wz, offset_y = new_y, real=True)
            hero.y = new_y
            displayHero(displaySurf, hero)
            pygame.display.update()
    elif hero.direction == RIGHT:
        for new_x in range(MAX_X - BOXSIZE, MIN_X, 0 - (BOXSIZE / 3)):
            world.drawWorld(displaySurf, wx, wy, wz, offset_x = new_x - MAX_X - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(displaySurf, wx + 1, wy, wz, offset_x = new_x, real=True)
            hero.x = new_x
            displayHero(displaySurf, hero)
            pygame.display.update()
    elif hero.direction == UP:
        for new_y in range(MIN_Y, MAX_Y, (BOXSIZE / 3)):
            world.drawWorld(displaySurf, wx, wy, wz, offset_y = new_y + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(displaySurf, wx, wy - 1, wz, offset_y = new_y - MAX_Y, real=True)
            hero.y = new_y
            displayHero(displaySurf, hero)
            pygame.display.update()
    elif hero.direction == LEFT:
        for new_x in range(MIN_X, MAX_X, (BOXSIZE / 3)):
            world.drawWorld(displaySurf, wx, wy, wz, offset_x = new_x + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(displaySurf, wx - 1, wy, wz, offset_x = new_x - MAX_X, real=True)
            hero.x = new_x
            displayHero(displaySurf, hero)
            pygame.display.update()

def createProjectile (projectileRef, direction, x, y):
    tempState.projectiles.append(Projectile(projectileRef, direction, x, y))
    
def moveAndDisplayProjectiles (displaySurf, wz, wx, wy): 
    # TODO: projectiles should eventually be able to hit hero
    filter = INCLUDE_OBSTACLES | INCLUDE_PUSHABLES | INCLUDE_LOCKED_DOORS
    obstacles = tempState.getObstacles(filter)
    for projectile in tempState.projectiles:
        if projectile.owner == -1:
            hitResult = projectile.move(obstacles, None, tempState.getCreatureRects())
        else:    
            hitResult = projectile.move(obstacles, permState.hero.rect, tempState.getCreatureRects(owner))
        if hitResult[0] != None or hitResult[1] != None or hitResult[2] != None or hitResult[3] != None:
            projectile.surface = None
        else:                    
            displaySurf.blit(projectile.surface, (projectile.x, projectile.y))
        if hitResult[3] != None:
            del tempState.creatures[hitResult[3]]
            if len(tempState.creatures) == 0:
                items.showHiddenItems()
    tempState.projectiles[:] = [p for p in tempState.projectiles if p.surface != None]

def createCreature (spriteRef, tx, ty):
    spriteType = spriteMap[spriteRef]
    if spriteType.type == ENEMY:
        tempState.creatures.append(Creature(spriteType.crossReference, tx, ty))
    else:
        tempState.allies.append((spriteRef, tx * BOXSIZE, ty * BOXSIZE))

def moveAndDisplayCreatures (displaySurf, wz, wx, wy):
    for idx, creature in enumerate(tempState.creatures):
        creature.tick()
        if creature.creatureType.movement == MOVE_FLY:
            filter = INCLUDE_OBSTACLES | INCLUDE_LOCKED_DOORS | INCLUDE_FAKE_OBSTACLES | INCLUDE_PUSHABLES
        elif creature.creatureType.movement == MOVE_SWIM:
            filter = INCLUDE_OBSTACLES | INCLUDE_LOCKED_DOORS | INCLUDE_FAKE_OBSTACLES | INCLUDE_PUSHABLES |\
                INCLUDE_CLEAR_OBSTACLES | INCLUDE_POISON_OBSTACLES | INCLUDE_FAKE_POISON_OBSTACLES
        elif creature.creatureType.movement == MOVE_POISON:
            filter = INCLUDE_OBSTACLES | INCLUDE_LOCKED_DOORS | INCLUDE_FAKE_OBSTACLES | INCLUDE_PUSHABLES |\
                INCLUDE_CLEAR_OBSTACLES | INCLUDE_WATER_OBSTACLES | INCLUDE_FAKE_WATER_OBSTACLES
        else:
            filter = INCLUDE_OBSTACLES | INCLUDE_WATER_OBSTACLES | INCLUDE_PUSHABLES | INCLUDE_FAKE_OBSTACLES |\
                INCLUDE_FAKE_WATER_OBSTACLES | INCLUDE_LOCKED_DOORS | INCLUDE_POISON_OBSTACLES |\
                INCLUDE_FAKE_POISON_OBSTACLES
        creatureObstacles = tempState.getObstacles(filter)
        hitResult = creature.move(creatureObstacles, permState.hero.rect, tempState.getCreatureRects(idx))
        if hitResult[0] != None or hitResult[1] != None or hitResult[2] != None or hitResult[3] != None:
            creature.changeDirection()
        displayCreature(displaySurf, creature)
    for ally in tempState.allies:
        spriteRef, x, y = ally[0], ally[1], ally[2]
        displayImage(displaySurf, spriteRef, DOWN, 0, x, y)

def getCreatureRefBySpriteRef (spriteRef):
    return spriteMap[spriteRef].crossReference

def displayStairs (displaySurf):
    stairIcon = 'FA'
    if permState.wz > 0: stairIcon = 'FB'
    if tempState.stairs != None and tempState.stairs[2] == VISIBLE:
        displayFeature(displaySurf, stairIcon, tempState.stairs[0], tempState.stairs[1])

def displayPushables (displaySurf):
    for pushable in tempState.pushables:
        displayPushable(displaySurf, pushable.featureRef, pushable.rect.x, pushable.rect.y)

def displayAvailableItems (displaySurf):
    for availableItem in tempState.availableItems:
        if availableItem.showState == VISIBLE and not permState.alreadyObtained(
                permState.wz, permState.wx, permState.wy, availableItem.x, availableItem.y):
            displayFeature(displaySurf, availableItem.itemType.id, availableItem.x, availableItem.y)

def displayDoors (displaySurf):
    for door in tempState.doors:
        doorIcon = 'FD' if door.isOpen() else 'FE'
        displayFeature(displaySurf, doorIcon, door.x, door.y)
