import pygame, sys, time, world, random
from pygame.locals import *
from constants import *
from movables import *
from state import tempState, permState

imageMap = {
    'LIFE': (25, 0)
}

terrainMap = {
    # x_offset, y_offset, r, g, b, obstacle (1=clear, 2=obstacle, 3=special)
    # nothing, grass
    '-': (0, 0, 255, 250, 205, 1), 'A': (0, 15, 0, 128, 0, 1), 
    # dungeon floor, brown brick wall, water, stones    
    'H': (5, 18, 105, 105, 105, 1), 'I': (8, 16, 139, 37, 0, 2), 'B': (37, 19, 0, 238, 238, 3), 'C': (53, 16, 139, 90, 0, 2),
    # colortile, large tiles, gray brick wall
    'J': (59, 15, 255, 250, 205, 1), 'K': (57, 15, 142, 142, 56, 1), 'L': (52, 17, 183, 183, 183, 2), 
    # sand
    'D': (7, 15, 205, 179, 139, 1),
    # cobblestone, poison swamp, lava, soft tile
    'F': (9, 14, 139, 136, 120, 1), 'E': (23, 19, 118, 238, 0, 3), 'M': (52, 13, 238, 0, 0, 2), 'N': (56, 16, 125, 158, 192, 1), 
    # murky water, bridge
    'O': (19, 19, 56, 142, 142, 3), 'G': (43, 16, 139, 0, 0, 1)
    # animated water: 36, 19 - 39, 19, animated swamp 23, 19 - 24, 19
    # animated lava: 49, 13 - 52, 13
}

featureMap = {
    # stairs to dungeon, stairs to overworld, blue tile, open door, closed door
    'FA': (15, 15, 3), 'FB': (31, 15, 3), 'FC': (29, 16, 4), 'FD': (27, 11, 1), 'FE': (23, 11, 2), 
    # tree
    'FF': (14, 18, 2),
    # statue, fountain, wings, armor, book
    'FG': (28, 11, 4), 'FH': (63, 11, 2), 'IA': (15, 7, 5), 'IB': (28, 21, 5), 'IC': (58, 22, 5), 
    # shield
    'ID': (54, 22, 5),
    # meat, gold, potion, bracelet, staff
    'IE': (36, 23, 5), 'IF': (59, 23, 5), 'IG': (63, 24, 5), 'IH': (60, 25, 5), 'II': (4, 46, 5), 
    # sword
    'IJ': (43, 27, 5),
    # chest, key, glove, boots, cloak
    'IK': (43, 45, 5), 'IL': (54, 45, 5), 'IM': (13, 21, 5), 'IN': (61, 20, 5), 'IO': (5, 21, 5),
    # amulet
    'IP': (15, 20, 5),
    # mirror, lantern, ring
    'IQ': (57, 45, 5), 'IR': (14, 24, 5), 'IS': (58, 25, 5),
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
    print spriteType.name, x, y, (x_offset, y_offset, BOXSIZE, BOXSIZE)
    displaySurf.blit(spriteType.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))                

def displayHero (displaySurf, hero):
    frame = 1 if hero.step == 3 else hero.step
    spriteType = hero.heroType.spriteType
    x_offset = (spriteType.coords[hero.direction][0] + frame) * BOXSIZE
    y_offset = (spriteType.coords[hero.direction][1]) * BOXSIZE
    displaySurf.blit(spriteType.name, (hero.x, hero.y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayAddition (displaySurf, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    displaySurf.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def scrollScreen (displaySurf, hero, wx, wy, wz):
    if hero.direction == DOWN:
        for new_y in range(MAX_Y, MIN_Y, 0 - (BOXSIZE / 3)):
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
    obstacles = world.getObstacles()
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
    tempState.projectiles[:] = [p for p in tempState.projectiles if p.surface != None]

def createCreature (spriteRef, tx, ty):
    spriteType = spriteMap[spriteRef]
    if spriteType.type == ENEMY:
        tempState.creatures.append(Creature(spriteType.crossReference, tx, ty))
    else:
        tempState.allies.append((spriteRef, tx * BOXSIZE, ty * BOXSIZE))

def moveAndDisplayCreatures (displaySurf, wz, wx, wy):
    obstacles = world.getObstacles()
    for idx, creature in enumerate(tempState.creatures):
        creature.tick()
        hitResult = creature.move(obstacles, permState.hero.rect, tempState.getCreatureRects(idx))
        if hitResult[0] != None or hitResult[1] != None or hitResult[2] != None or hitResult[3] != None:
            creature.changeDirection()
        displayCreature(displaySurf, creature)
    for ally in tempState.allies:
        spriteRef, x, y = ally[0], ally[1], ally[2]
        displayImage(displaySurf, spriteRef, DOWN, 0, x, y)

def getCreatureRefBySpriteRef (spriteRef):
    return spriteMap[spriteRef].crossReference
