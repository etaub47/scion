import pygame, random
from constants import *
from pygame import Rect
from pygame.locals import SRCALPHA

sprite1 = pygame.image.load('../img/sprite1.png')
sprite2 = pygame.image.load('../img/sprite2.png')
sprite3 = pygame.image.load('../img/sprite3.png')
sprite4 = pygame.image.load('../img/sprite4.png')
sprite5 = pygame.image.load('../img/sprite5.png')
sprite6 = pygame.image.load('../img/sprite6.png')

class SpriteType:
    def __init__ (self, name, type, coords, size, crossReference):
        self.name, self.type, self.coords, self.size, self.crossReference = name, type, coords, size, crossReference

spriteMap = {
    'S1': SpriteType(sprite2, HERO, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'H1'), 
    'S2': SpriteType(sprite2, HERO, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'H2'),
    'S3': SpriteType(sprite2, HERO, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'H3'), 
    'S4': SpriteType(sprite2, HERO, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'H4'), 
    'S5': SpriteType(sprite2, HERO, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'H5'),
    'S6': SpriteType(sprite2, HERO, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'H6'), 
    'S7': SpriteType(sprite2, HERO, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'H7'),
    'S8': SpriteType(sprite2, HERO, [(9, 4), (9, 5), (9, 6), (9, 7)], BOXSIZE, 'H8'),
    'S9': SpriteType(sprite3, HERO, [(0, 0), (9, 0), (3, 0), (6, 0)], BOXSIZE, 'H9'), 
    'S10': SpriteType(sprite3, ENEMY, [(0, 1), (9, 1), (3, 1), (6, 1)], BOXSIZE, 'H10'),    
    'S11': SpriteType(sprite3, ENEMY, [(0, 2), (9, 2), (3, 2), (6, 2)], BOXSIZE, 'C11'), # goblin
    'S12': SpriteType(sprite3, ENEMY, [(0, 3), (9, 3), (3, 3), (6, 3)], BOXSIZE, 'C12'),    
    'S13': SpriteType(sprite3, ENEMY, [(0, 4), (9, 4), (3, 4), (6, 4)], BOXSIZE, 'C13'), # water demon
    'S14': SpriteType(sprite3, ENEMY, [(0, 5), (9, 5), (3, 5), (6, 5)], BOXSIZE, 'C14'),
    'S15': SpriteType(sprite3, ENEMY, [(0, 6), (9, 6), (3, 6), (6, 6)], BOXSIZE, 'C15'),
    'S16': SpriteType(sprite3, ENEMY, [(0, 7), (9, 7), (3, 7), (6, 7)], BOXSIZE, 'C16'),
    'S17': SpriteType(sprite4, HERO, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'H17'), # girl
    'S18': SpriteType(sprite4, ENEMY, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'C18'),
    'S19': SpriteType(sprite4, ENEMY, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'C19'),
    'S20': SpriteType(sprite4, ENEMY, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'C20'),    
    'S21': SpriteType(sprite4, ENEMY, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'C21'), # worg
    'S22': SpriteType(sprite4, ENEMY, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'C22'),
    'S23': SpriteType(sprite4, ENEMY, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'C23'),
    'S24': SpriteType(sprite6, ENEMY, [(0, 0), (0, 1), (0, 2), (0, 3)], BOXSIZE, 'C24'),
    'S25': SpriteType(sprite5, ENEMY, [(3, 0), (3, 1), (3, 2), (3, 3)], BOXSIZE, 'C25'),
    'S26': SpriteType(sprite6, ENEMY, [(6, 0), (6, 1), (6, 2), (6, 3)], BOXSIZE, 'C26'),
    'S27': SpriteType(sprite5, ENEMY, [(9, 0), (9, 1), (9, 2), (9, 3)], BOXSIZE, 'C27'),
    'S28': SpriteType(sprite5, ENEMY, [(0, 4), (0, 5), (0, 6), (0, 7)], BOXSIZE, 'C28'),
    'S29': SpriteType(sprite6, ENEMY, [(3, 4), (3, 5), (3, 6), (3, 7)], BOXSIZE, 'C29'),
    'S30': SpriteType(sprite6, ENEMY, [(6, 4), (6, 5), (6, 6), (6, 7)], BOXSIZE, 'C30'),
    'S31': SpriteType(sprite5, ENEMY, [(9, 4), (9, 5), (9, 6), (9, 7)], BOXSIZE, 'C31')
}

class CreatureType:
    def __init__ (self, spriteRef, pattern, speed):
        self.spriteType, self.pattern, self.speed = spriteMap[spriteRef], pattern, speed

creatureMap = {
    'C11': CreatureType('S11', PATTERN_RANDOM, 5), # goblin    
    'C13': CreatureType('S13', PATTERN_RANDOM, 5), # water demon
    'C14': CreatureType('S14', PATTERN_RANDOM, 5),
    'C16': CreatureType('S16', PATTERN_RANDOM, 5),
    'C19': CreatureType('S19', PATTERN_RANDOM, 5),    
    'C21': CreatureType('S21', PATTERN_RANDOM, 8), # worg
    'C23': CreatureType('S23', PATTERN_RANDOM, 5),
    'C24': CreatureType('S24', PATTERN_RANDOM, 5),
    'C29': CreatureType('S29', PATTERN_RANDOM, 5)
}
        
class ProjectileType:
    def __init__ (self, sx, sy, rotateOffset, speed, rotateInd, size):
        self.sx, self.sy, self.rotateOffset, self.speed = sx, sy, rotateOffset, speed
        self.rotateInd, self.size = rotateInd, size
        
projectileMap = {
    'PA': ProjectileType(55, 46, 45, 25, True, BOXSIZE / 4), # arrow
    'PB': ProjectileType(3, 43, 45, 25, True, BOXSIZE / 2),  # fire arrow
    'PC': ProjectileType(29, 43, 45, 20, True, BOXSIZE / 2), # ice shard
    'PD': ProjectileType(22, 47, 0, 15, False, BOXSIZE / 2), # tornado
    'PE': ProjectileType(9, 43, -45, 20, True, BOXSIZE / 2), # fireball
    'PF': ProjectileType(10, 11, 90, 15, True, BOXSIZE / 2), # web
    'PG': ProjectileType(2, 11, 0, 25, True, BOXSIZE / 2),   # dagger
    'PH': ProjectileType(37, 47, 135, 20, True, BOXSIZE / 2) # spear
}

class HeroType:
    def __init__ (self, spriteRef, speed):
        self.spriteType, self.speed = spriteMap[spriteRef], speed

heroMap = {
    'H1': HeroType('S1', 5),   #
    'H2': HeroType('S2', 5),   #
    'H3': HeroType('S3', 5),   #
    'H4': HeroType('S4', 5),   #
    'H5': HeroType('S5', 5),   #
    'H6': HeroType('S6', 5),   #
    'H7': HeroType('S7', 5),   #
    'H8': HeroType('S8', 5),   #
    'H9': HeroType('S9', 5),   #
    'H10': HeroType('S10', 5), #
    'H17': HeroType('S17', 5)  #
}

class Movable:
    """ a base class representing something that can move, e.g. active hero, creature, projectile """
    def __init__ (self, direction, x, y, speed, pattern, step, timer, rect):
        self.direction, self.x, self.y, self.speed = direction, x, y, speed
        self.pattern, self.step, self.timer, self.rect = pattern, step, timer, rect
    def changeDirection (self):
        newDirection = self.direction
        while newDirection == self.direction: 
            newDirection = random.randint(0, 3)
        self.direction = newDirection        
    def move (self, obstacles, hero, creatures):
        origLeft, origTop = self.rect.left, self.rect.top
        hitEdge, hitObstacle, hitHero, hitCreature = None, None, None, None
        if self.direction == DOWN:
            self.rect.move_ip(0, self.speed)            
            if self.rect.bottom >= MAX_Y: hitEdge, self.rect.bottom = self.direction, MAX_Y
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.bottom = idx, obstacles[idx].top
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.bottom = True, hero.top            
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.bottom = idx, creatures[idx].top
        elif self.direction == RIGHT:
            self.rect.move_ip(self.speed, 0)
            if self.rect.right >= MAX_X: hitEdge, self.rect.right = self.direction, MAX_X
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.right = idx, obstacles[idx].left
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.right = True, hero.left            
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.right = idx, creatures[idx].left
        elif self.direction == UP:
            self.rect.move_ip(0, -self.speed)            
            if self.rect.top <= MIN_Y: hitEdge, self.rect.top = self.direction, MIN_Y
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.top = idx, obstacles[idx].bottom
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.top = True, hero.bottom            
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.top = idx, creatures[idx].bottom
        elif self.direction == LEFT:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.left <= MIN_X: hitEdge, self.rect.left = self.direction, MIN_X
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.left = idx, obstacles[idx].right
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.left = True, hero.right            
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.left = idx, creatures[idx].right
        self.x += (self.rect.left - origLeft)
        self.y += (self.rect.top - origTop)
        if self.pattern == PATTERN_RANDOM:
            if hitObstacle or hitEdge or self.timer == 50 or random.randint(1, 100) <= 2:
                self.changeDirection()
        return (hitEdge, hitObstacle, hitHero, hitCreature)

class Creature (Movable):
    def __init__ (self, creatureRef, tx, ty):
        self.creatureType = creatureMap[creatureRef]
        size = self.creatureType.spriteType.size
        rect = Rect(tx * size + 3, ty * size + (size / 2), size - 6, size / 2)
        Movable.__init__(self, random.randint(0, 3), tx * size, ty * size, self.creatureType.speed,
            self.creatureType.pattern, 0, 0, rect)
    def tick (self):
        self.timer += 1
        if self.timer > 100: self.timer = 0
        if self.timer % 2 == 0: self.step += 1
        if self.step >= 4: self.step = 0    

class Hero (Creature):
    def __init__ (self, heroRef, tx, ty):
        self.heroType = heroMap[heroRef]
        rect = Rect(tx * BOXSIZE + 3, ty * BOXSIZE + (BOXSIZE / 2), BOXSIZE - 6, BOXSIZE / 2)
        Movable.__init__(self, DOWN, tx * BOXSIZE, ty * BOXSIZE, 0, PATTERN_NONE, 0, 0, rect)
    def moving (self, direction):
        self.direction, self.speed = direction, self.heroType.speed
    def stop (self):
        self.speed = 0
    def updateRect (self):
        self.rect = Rect(self.x + 3, self.y + (BOXSIZE / 2), BOXSIZE - 6, BOXSIZE / 2)

class Projectile (Movable):
    def __init__ (self, projectileRef, direction, x, y, owner):
        self.projectileType, self.owner, angle = projectileMap[projectileRef], owner, 0
        size = self.projectileType.size
        if self.projectileType.rotateInd:
            angle = self.projectileType.rotateOffset
            if direction == DOWN: angle += 90
            elif direction == RIGHT: angle += 180
            elif direction == UP: angle += 270        
        rect = Rect(x + (BOXSIZE / 2 - size / 2), y + (BOXSIZE / 2 - size / 2), size, size)
        self.surface = pygame.Surface((BOXSIZE, BOXSIZE), SRCALPHA)
        self.surface.blit(sprite1, (0, 0), area=(self.projectileType.sx * BOXSIZE, 
            self.projectileType.sy * BOXSIZE, BOXSIZE, BOXSIZE))
        self.surface = pygame.transform.rotate(self.surface, angle)
        Movable.__init__(self, direction, x, y, self.projectileType.speed, PATTERN_STRAIGHT, 0, 0, rect)
