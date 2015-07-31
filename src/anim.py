import pygame, sys, time, world, random
from pygame.locals import *
from constants import *

sprite1 = pygame.image.load('../img/sprite1.png')
sprite2 = pygame.image.load('../img/sprite2.png')
sprite3 = pygame.image.load('../img/sprite3.png')
sprite4 = pygame.image.load('../img/sprite4.png')
sprite5 = pygame.image.load('../img/sprite5.png')
sprite6 = pygame.image.load('../img/sprite6.png')

spriteMap = { 
    'S1': (sprite2, [(0, 0), (0, 1), (0, 2), (0, 3)], 'H1'), 
    'S2': (sprite2, [(3, 0), (3, 1), (3, 2), (3, 3)], 'H2'),
    'S3': (sprite2, [(6, 0), (6, 1), (6, 2), (6, 3)], 'H3'), 
    'S4': (sprite2, [(9, 0), (9, 1), (9, 2), (9, 3)], 'H4'), 
    'S5': (sprite2, [(0, 4), (0, 5), (0, 6), (0, 7)], 'H5'),
    'S6': (sprite2, [(3, 4), (3, 5), (3, 6), (3, 7)], 'H6'), 
    'S7': (sprite2, [(6, 4), (6, 5), (6, 6), (6, 7)], 'H7'),
    'S8': (sprite2, [(9, 4), (9, 5), (9, 6), (9, 7)], 'H8'),
    'S9': (sprite3, [(0, 0), (9, 0), (3, 0), (6, 0)], 'H9'), 
    'S10': (sprite3, [(0, 1), (9, 1), (3, 1), (6, 1)], 'H10'),
    # goblin
    'S11': (sprite3, [(0, 2), (9, 2), (3, 2), (6, 2)], 'C11'),
    'S12': (sprite3, [(0, 3), (9, 3), (3, 3), (6, 3)], 'C12'),
    # water demon
    'S13': (sprite3, [(0, 4), (9, 4), (3, 4), (6, 4)], 'C13'), 
    'S14': (sprite3, [(0, 5), (9, 5), (3, 5), (6, 5)], 'C14'),
    'S15': (sprite3, [(0, 6), (9, 6), (3, 6), (6, 6)], 'C15'),
    'S16': (sprite3, [(0, 7), (9, 7), (3, 7), (6, 7)], 'C16'),
    'S17': (sprite4, [(0, 0), (0, 1), (0, 2), (0, 3)], 'C17'), 
    'S18': (sprite4, [(3, 0), (3, 1), (3, 2), (3, 3)], 'C18'),
    'S19': (sprite4, [(6, 0), (6, 1), (6, 2), (6, 3)], 'C19'),
    'S20': (sprite4, [(9, 0), (9, 1), (9, 2), (9, 3)], 'C20'),
    # worg
    'S21': (sprite4, [(0, 4), (0, 5), (0, 6), (0, 7)], 'C21'),
    'S22': (sprite4, [(3, 4), (3, 5), (3, 6), (3, 7)], 'C22'),
    'S23': (sprite4, [(6, 4), (6, 5), (6, 6), (6, 7)], 'C23'),
    'S24': (sprite6, [(0, 0), (0, 1), (0, 2), (0, 3)], 'C24'),
    'S25': (sprite5, [(3, 0), (3, 1), (3, 2), (3, 3)], 'C25'),
    'S26': (sprite6, [(6, 0), (6, 1), (6, 2), (6, 3)], 'C26'),
    'S27': (sprite5, [(9, 0), (9, 1), (9, 2), (9, 3)], 'C27'),
    'S28': (sprite5, [(0, 4), (0, 5), (0, 6), (0, 7)], 'C28'),
    'S29': (sprite6, [(3, 4), (3, 5), (3, 6), (3, 7)], 'C29'),
    'S30': (sprite6, [(6, 4), (6, 5), (6, 6), (6, 7)], 'C30'),
    'S31': (sprite5, [(9, 4), (9, 5), (9, 6), (9, 7)], 'C31')
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

projectileMap = {
    # 'identifier': (x_offset, y_offset, rotate_angle_offset, speed, rotate?)
    # arrow, fire arrow, ice shard
    # tornado, fireball, web
    # dagger, spear
    'PA': (55, 46, 45, 25, True), 'PB': (3, 43, 45, 25, True), 'PC': (29, 43, 45, 20, True), 
    'PD': (22, 47, 0, 15, False), 'PE': (9, 43, -45, 20, True), 'PF': (10, 11, 90, 15, True),
    'PG': (2, 11, 0, 25, True), 'PH': (37, 47, 135, 20, True)
}

creatureMap = {
    # 'identifier': (sprite_ref, pattern, speed)
    # pattern: 0 = random
    # goblin
    'C11': ('S11', 0, 5), 
    # water demon
    'C13': ('S13', 0, 5),
    'C14': ('S14', 0, 5),
    'C16': ('S16', 0, 5),
    'C19': ('S19', 0, 5),
    # worg
    'C21': ('S21', 0, 8),
    'C23': ('S23', 0, 5),
    'C24': ('S24', 0, 5),
    'C29': ('S29', 0, 5)
}

heroMap = {
    'H1': ('S1', 0),
    'H2': ('S2', 0),
    'H3': ('S3', 0),
    'H4': ('S4', 0),
    'H5': ('S5', 0),
    'H6': ('S6', 0),
    'H7': ('S7', 0),
    'H8': ('S8', 0),
    'H9': ('S9', 0),
    'H10': ('S10', 0)
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

def displayImage (DISPLAYSURF, imageRef, direction, step, x, y):
    sprite = spriteMap[imageRef]
    if step == 3: step = 1
    x_offset = (sprite[1][direction][0] + step) * BOXSIZE
    y_offset = (sprite[1][direction][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite[0], (x, y), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))

def displayTerrain (DISPLAYSURF, terrainRef, x, y, offset_x = 0, offset_y = 0):
    if terrainRef in terrainMap:
        x_offset = (terrainMap[terrainRef][0]) * BOXSIZE
        y_offset = (terrainMap[terrainRef][1]) * BOXSIZE
        DISPLAYSURF.blit(sprite1, (x * BOXSIZE + offset_x, y * BOXSIZE + offset_y), 
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

def displayCreature (DISPLAYSURF, spriteRef, x, y, direction = DOWN, step = 1):
    displayImage(DISPLAYSURF, spriteRef, direction, step, x, y)

def displayAddition (DISPLAYSURF, additionRef, x, y):
    if additionRef[-1] == '\n': 
        additionRef = additionRef[:-1]
    x_offset = (additionMap[additionRef][0]) * BOXSIZE
    y_offset = (additionMap[additionRef][1]) * BOXSIZE
    DISPLAYSURF.blit(sprite1, (x * BOXSIZE, y * BOXSIZE), area=(x_offset + 1, y_offset, BOXSIZE - 1, BOXSIZE))

def scrollScreen (DISPLAYSURF, i, direction, step, x, y, wx, wy, wz):
    if direction == DOWN:
        for new_y in range(MAX_Y, MIN_Y, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y - MAX_Y - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy + 1, wz, offset_y = new_y, real=True)
            displayImage(DISPLAYSURF, i, direction, step, x, new_y)
            pygame.display.update()
    elif direction == RIGHT:
        for new_x in range(MAX_X, MIN_X, 0 - (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x - MAX_X - (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx + 1, wy, wz, offset_x = new_x, real=True)
            displayImage(DISPLAYSURF, i, direction, step, new_x, y)
            pygame.display.update()
    elif direction == UP:
        for new_y in range(MIN_Y, MAX_Y, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_y = new_y + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx, wy - 1, wz, offset_y = new_y - MAX_Y, real=True)
            displayImage(DISPLAYSURF, i, direction, step, x, new_y)
            pygame.display.update()
    elif direction == LEFT:
        for new_x in range(MIN_X, MAX_X, (BOXSIZE / 3)):
            world.drawWorld(DISPLAYSURF, wx, wy, wz, offset_x = new_x + (BOXSIZE * 2 / 3), real=True)
            world.drawWorld(DISPLAYSURF, wx - 1, wy, wz, offset_x = new_x - MAX_X, real=True)
            displayImage(DISPLAYSURF, i, direction, step, new_x, y)
            pygame.display.update()

def createProjectile (projectileRef, direction, x, y):
    x_offset = (projectileMap[projectileRef][0]) * BOXSIZE
    y_offset = (projectileMap[projectileRef][1]) * BOXSIZE
    rot_angle = projectileMap[projectileRef][2]
    speed = projectileMap[projectileRef][3]
    if not projectileMap[projectileRef][4]: rot_angle = 0
    elif direction == DOWN: rot_angle += 90
    elif direction == RIGHT: rot_angle += 180
    elif direction == UP: rot_angle += 270
    proj_surface = pygame.Surface((BOXSIZE, BOXSIZE), SRCALPHA)
    proj_surface.blit(sprite1, (0, 0), area=(x_offset, y_offset, BOXSIZE, BOXSIZE))
    proj_surface = pygame.transform.rotate(proj_surface, rot_angle)
    projectiles.append([proj_surface, direction, x, y, speed])
    
def move (item, wz, wx, wy):
    # item = [something, direction, x, y, speed]
    # returns True if the move resulted in a collision with terrain or a feature
    if (item[DIR_IDX] == DOWN):
        rect = Rect(item[X_IDX] + 2, item[Y_IDX] + BOXSIZE / 2, BOXSIZE - 4, BOXSIZE / 2)
        if item[Y_IDX] >= MAX_Y or world.move(wz, wx, wy, rect, 0, item[SPEED_IDX]):
            item[X_IDX], item[Y_IDX] = rect.x - 2, rect.y - BOXSIZE / 2
            return True
    elif item[DIR_IDX] == RIGHT:
        rect = Rect(item[X_IDX] + 2, item[Y_IDX] + BOXSIZE / 2, BOXSIZE - 4, BOXSIZE / 2)
        if item[X_IDX] >= MAX_X or world.move(wz, wx, wy, rect, item[SPEED_IDX], 0):
            item[X_IDX], item[Y_IDX] = rect.x - 2, rect.y - BOXSIZE / 2
            return True
    elif item[DIR_IDX] == UP:
        rect = Rect(item[X_IDX] + 2, item[Y_IDX] + BOXSIZE / 2, BOXSIZE - 4, BOXSIZE / 2)
        if item[Y_IDX] <= MIN_Y or world.move(wz, wx, wy, rect, 0, -item[SPEED_IDX]):
            item[X_IDX], item[Y_IDX] = rect.x - 2, rect.y - BOXSIZE / 2
            return True
    elif item[DIR_IDX] == LEFT:
        rect = Rect(item[X_IDX] + 2, item[Y_IDX] + BOXSIZE / 2, BOXSIZE - 4, BOXSIZE / 2)
        if item[X_IDX] <= MIN_X or world.move(wz, wx, wy, rect, -item[SPEED_IDX], 0):
            item[X_IDX], item[Y_IDX] = rect.x - 2, rect.y - BOXSIZE / 2
            return True
    item[X_IDX], item[Y_IDX] = rect.x - 2, rect.y - BOXSIZE / 2
    return False
    
def moveAndDisplayProjectiles (DISPLAYSURF, wz, wx, wy):    
    for projectile in projectiles:
        DISPLAYSURF.blit(projectile[SOURCE_IDX], (projectile[X_IDX], projectile[Y_IDX]))
        if move(projectile, wz, wx, wy): # move the projectile and check to see if it went off screen
            projectile[SOURCE_IDX] = None
    projectiles[:] = [p for p in projectiles if p[0] != None]

def createCreature (creatureRef, x, y):
    if creatureRef[0] == 'C':
        sprite_ref = creatureMap[creatureRef][0]
        pattern = creatureMap[creatureRef][1]
        speed = creatureMap[creatureRef][2]
        direction = random.randint(0, 3)
        creatures.append([sprite_ref, direction, x * BOXSIZE, y * BOXSIZE, speed, pattern, 0, 0])
    else:
        sprite_ref = heroMap[creatureRef][0]
        staticHeroes.append((sprite_ref, x * BOXSIZE, y * BOXSIZE))

def moveAndDisplayCreatures (DISPLAYSURF, wz, wx, wy):
    for creature in creatures:
        displayCreature(DISPLAYSURF, creature[SPRITE_IDX], creature[X_IDX], creature[Y_IDX],
            direction = creature[DIR_IDX], step = creature[STEP_IDX])
        if creature[TIMER_IDX] % 2 == 0:
            creature[STEP_IDX] += 1
        creature[TIMER_IDX] += 1
        if creature[TIMER_IDX] > 100:
            creature[TIMER_IDX] = 0
        if creature[STEP_IDX] >= 4: creature[STEP_IDX] = 0
        if creature[PATTERN_IDX] == 0:
            if move(creature, wz, wx, wy) or creature[TIMER_IDX] == 50 or random.randint(1, 100) <= 2:
                newDirection = random.randint(0, 3)
                creature[DIR_IDX] = newDirection
    for hero in staticHeroes:
        spriteRef, x, y = hero[0], hero[1], hero[2]
        displayCreature(DISPLAYSURF, spriteRef, x, y)

def getCreatureRefBySpriteRef (spriteRef):
    return spriteMap[spriteRef][2]

def clearCreatures ():
    creatures[:] = []
