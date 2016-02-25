import pygame, sys, time, world, random

from pygame.locals import *
from constants import *
from movables import *
from state import tempState, permState

def scrollScreen (displaySurf, hero, wx, wy, wz):
    if hero.direction == DOWN:
        for new_y in range(MAX_Y - BOXSIZE, MIN_Y, 0 - (BOXSIZE / 3)):
            world.drawMap(displaySurf, wx, wy, wz, offset_y = new_y - MAX_Y - (BOXSIZE * 2 / 3), real=True)
            world.drawMap(displaySurf, wx, wy + 1, wz, offset_y = new_y, real=True)
            hero.y = new_y
            hero.draw(displaySurf)
            pygame.display.update()
    elif hero.direction == RIGHT:
        for new_x in range(MAX_X - BOXSIZE, MIN_X, 0 - (BOXSIZE / 3)):
            world.drawMap(displaySurf, wx, wy, wz, offset_x = new_x - MAX_X - (BOXSIZE * 2 / 3), real=True)
            world.drawMap(displaySurf, wx + 1, wy, wz, offset_x = new_x, real=True)
            hero.x = new_x
            hero.draw(displaySurf)
            pygame.display.update()
    elif hero.direction == UP:
        for new_y in range(MIN_Y, MAX_Y, (BOXSIZE / 3)):
            world.drawMap(displaySurf, wx, wy, wz, offset_y = new_y + (BOXSIZE * 2 / 3), real=True)
            world.drawMap(displaySurf, wx, wy - 1, wz, offset_y = new_y - MAX_Y, real=True)
            hero.y = new_y
            hero.draw(displaySurf)
            pygame.display.update()
    elif hero.direction == LEFT:
        for new_x in range(MIN_X, MAX_X, (BOXSIZE / 3)):
            world.drawMap(displaySurf, wx, wy, wz, offset_x = new_x + (BOXSIZE * 2 / 3), real=True)
            world.drawMap(displaySurf, wx - 1, wy, wz, offset_x = new_x - MAX_X, real=True)
            hero.x = new_x
            hero.draw(displaySurf)
            pygame.display.update()

def moveProjectiles (displaySurf): 
    filter = INCLUDE_OBSTACLES | INCLUDE_PUSHABLES | INCLUDE_LOCKED_DOORS
    obstacles = tempState.getObstacles(filter)
    for projectile in tempState.projectiles:
        if projectile.owner == -1:
            hitResult = projectile.move(obstacles, None, tempState.getCreatureRects())
        else:    
            hitResult = projectile.move(obstacles, tempState.hero.rect, tempState.getCreatureRects(owner))
        if hitResult[0] != None or hitResult[1] != None or hitResult[2] != None or hitResult[3] != None:
            projectile.surface = None
        if hitResult[3] != None:
            del tempState.creatures[hitResult[3]]
            if len(tempState.creatures) == 0:
                items.showHiddenItems()
    tempState.projectiles[:] = [p for p in tempState.projectiles if p.surface != None]

def moveCreatures (displaySurf):
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
        hitResult = creature.move(creatureObstacles, tempState.hero.rect, tempState.getCreatureRects(idx))
        if hitResult[0] != None or hitResult[1] != None or hitResult[2] != None or hitResult[3] != None:
            creature.changeDirection()
