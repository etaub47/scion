import pygame, sys, time, world, random
from pygame.locals import *
from constants import *
from movables import *

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

projectiles = []
creatures = []
staticHeroes = []

def getTerrainColor (terrainRef):
    return terrainMap[terrainRef][2:5]
    
def getTerrainObstacle (terrainRef):
    return terrainMap[terrainRef][5]

def getFeatureObstacle (featureRef):
    return featureMap[featureRef][2]

def displaySimpleImage (DISPLAYSURF, imageRef, x, y):
    image = imageMap[imageRef]
    x_offset, y_offset = image[0] * BOXSIZE, image[1] * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
    
def displayLifeMeter (DISPLAYSURF, life):
    for heart in range(life):
        displaySimpleImage(DISPLAYSURF, 'LIFE', heart * (BOXSIZE / 3) - (BOXSIZE / 2), 0)        

def displayImage (DISPLAYSURF, spriteRef, direction, step, x, y):
    sprite = spriteMap[spriteRef]
    if step == 3: step = 1
    x_offset = (sprite.coords[direction][0] + step) * BOXSIZE
    y_offset = (sprite.coords[direction][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayTerrain (DISPLAYSURF, terrainRef, tx, ty, offset_x = 0, offset_y = 0):
    if terrainRef in terrainMap:
        x_offset = (terrainMap[terrainRef][0]) * BOXSIZE
        y_offset = (terrainMap[terrainRef][1]) * BOXSIZE
        DISPLAYSURF.blit(sprite1, (tx * BOXSIZE + offset_x, ty * BOXSIZE + offset_y), 
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

def displayCreature (DISPLAYSURF, creature):
    frame = 1 if creature.step == 3 else creature.step
    spriteType = creature.creatureType.spriteType
    x_offset = (spriteType.coords[creature.direction][0] + frame) * BOXSIZE
    y_offset = (spriteType.coords[creature.direction][1]) * BOXSIZE
    DISPLAYSURF.blit(spriteType.name, (creature.x, creature.y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayHero (DISPLAYSURF, hero, x, y):
    frame = 1 if hero.step == 3 else hero.step
    spriteType = hero.heroType.spriteType
    x_offset = (spriteType.coords[hero.direction][0] + frame) * BOXSIZE
    y_offset = (spriteType.coords[hero.direction][1]) * BOXSIZE
    DISPLAYSURF.blit(spriteType.name, (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayAddition (DISPLAYSURF, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def scrollScreen (DISPLAYSURF, hero, wx, wy, wz):
    if hero.direction == DOWN:
        for new_y in range(MAX_Y, MIN_Y, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y - MAX_Y - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy + 1, wz, offset_y = new_y, real=True)
            displayHero(DISPLAYSURF, hero, hero.x, new_y)
            pygame.display.update()
    elif hero.direction == RIGHT:
        for new_x in range(MAX_X - BOXSIZE, MIN_X, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x - MAX_X - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx + 1, wy, wz, offset_x = new_x, real=True)
            displayHero(DISPLAYSURF, hero, new_x, hero.y)
            pygame.display.update()
    elif hero.direction == UP:
        for new_y in range(MIN_Y, MAX_Y, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy - 1, wz, offset_y = new_y - MAX_Y, real=True)
            displayHero(DISPLAYSURF, hero, hero.x, new_y)
            pygame.display.update()
    elif hero.direction == LEFT:
        for new_x in range(MIN_X, MAX_X, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx - 1, wy, wz, offset_x = new_x - MAX_X, real=True)
            displayHero(DISPLAYSURF, hero, new_x, hero.y)
            pygame.display.update()

def createProjectile (projectileRef, direction, x, y):
    projectiles.append(Projectile(projectileRef, direction, x, y))
    
def moveAndDisplayProjectiles (DISPLAYSURF, wz, wx, wy):    
    obstacles = world.getObstacles()
    for projectile in projectiles:
        hitResult = projectile.move(obstacles, None, None) # TODO: hero, creatures
        if hitResult[0] or hitResult[1] or hitResult[2] or hitResult[3]:
            projectile.surface = None
        else:                    
            DISPLAYSURF.blit(projectile.surface, (projectile.x, projectile.y))
    projectiles[:] = [p for p in projectiles if p.surface != None]

def createCreature (spriteRef, tx, ty):
    spriteType = spriteMap[spriteRef]
    if spriteType.type == ENEMY:
        creatures.append(Creature(spriteType.crossReference, tx, ty))
    else:
        staticHeroes.append((spriteRef, tx * BOXSIZE, ty * BOXSIZE))

def moveAndDisplayCreatures (DISPLAYSURF, wz, wx, wy):
    obstacles = world.getObstacles()
    for creature in creatures:
        creature.tick()
        creature.move(obstacles, None, None) # TODO: hero, creatures
        displayCreature(DISPLAYSURF, creature)
    for hero in staticHeroes:
        spriteRef, x, y = hero[0], hero[1], hero[2]
        displayImage(DISPLAYSURF, spriteRef, DOWN, 0, x, y)

def getCreatureRefBySpriteRef (spriteRef):
    return spriteMap[spriteRef].crossReference

def clearCreatures ():
    projectiles[:] = []
    creatures[:] = []
    staticHeroes[:] = []
