import pygame, items, random
from constants import *
from pygame import Rect
from pygame.locals import SRCALPHA
from state import tempState, permState

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

class CreatureType:
    def __init__ (self, spriteRef, pattern, speed, movement):
        self.spriteType, self.pattern, self.speed = spriteMap[spriteRef], pattern, speed
        self.movement = movement

creatureMap = {
    'C7' : CreatureType('S7' , PATTERN_RANDOM, 5, MOVE_WALK), # one-eyed creep (unused)
    'C9' : CreatureType('S9' , PATTERN_RANDOM, 5, MOVE_FLY), # ghost
    'C10': CreatureType('S10', PATTERN_RANDOM, 5, MOVE_WALK), # skeleton
    'C11': CreatureType('S11', PATTERN_RANDOM, 5, MOVE_WALK), # goblin
    'C12': CreatureType('S12', PATTERN_RANDOM, 5, MOVE_WALK), # gargoyle
    'C13': CreatureType('S13', PATTERN_RANDOM, 5, MOVE_SWIM), # water demon
    'C14': CreatureType('S14', PATTERN_RANDOM, 5, MOVE_WALK), # red-haired woman
    'C15': CreatureType('S15', PATTERN_RANDOM, 5, MOVE_WALK), # grim reaper
    'C16': CreatureType('S16', PATTERN_RANDOM, 5, MOVE_WALK), # blue powerful mage
    'C19': CreatureType('S19', PATTERN_RANDOM, 5, MOVE_WALK), # white-haired mage
    'C20': CreatureType('S20', PATTERN_RANDOM, 5, MOVE_WALK), # zombie
    'C21': CreatureType('S21', PATTERN_RANDOM, 8, MOVE_WALK), # worg
    'C23': CreatureType('S23', PATTERN_RANDOM, 5, MOVE_WALK), # tan skeleton
    'C24': CreatureType('S24', PATTERN_RANDOM, 5, MOVE_WALK), # scorpion
    'C26': CreatureType('S26', PATTERN_RANDOM, 5, MOVE_WALK),
    'C27': CreatureType('S27', PATTERN_RANDOM, 5, MOVE_WALK),
    'C29': CreatureType('S29', PATTERN_RANDOM, 5, MOVE_WALK),
    'C30': CreatureType('S30', PATTERN_RANDOM, 5, MOVE_FLY)  # bat
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
    'H1': HeroType('S1', 5),   # main hero
    'H2': HeroType('S2', 5),   # blonde girl
    'H4': HeroType('S4', 5),   # blue-haired girl
    'H5': HeroType('S5', 5),   # long-haired caped dude
    'H6': HeroType('S6', 5),   # fancy girl
    'H8': HeroType('S8', 5),   # wizened old man
    'H17': HeroType('S17', 5)  # simple girl
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
    def move (self, obstacles, hero, creatures, pushables=None):
        origLeft, origTop = self.rect.left, self.rect.top
        hitEdge, hitObstacle, hitHero, hitCreature = None, None, None, None
        visibleItemRects = []
        
        if self.direction == DOWN:
            self.rect.move_ip(0, self.speed)            
            
            # check for collision with edge of screen
            if self.rect.bottom >= MAX_Y_2: hitEdge, self.rect.bottom = self.direction, MAX_Y_2
            
            # check for collision with pushables
            if pushables != None:
                idx = self.rect.collidelist(pushables)
                if idx >= 0:
                    tempState.pushables[idx].rect.move_ip(0, self.speed)
                    del pushables[idx]
                    rects = obstacles + creatures + pushables + \
                        tempState.getAvailableItemRects(visibleOnly=True)
                    idx2 = tempState.pushables[idx].rect.collidelist(rects)
                    if idx2 >= 0:
                        tempState.pushables[idx].rect.bottom = rects[idx2].top
                        self.rect.bottom = tempState.pushables[idx].rect.top
                    elif self.rect.bottom >= MAX_Y_2 - BOXSIZE:
                        tempState.pushables[idx].rect.bottom = MAX_Y_2
                        self.rect.bottom = tempState.pushables[idx].rect.top                        
                    elif tempState.pushables[idx].secretTrigger:
                        items.showSecretItem()
                        
            # check for collision with obstacles
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.bottom = idx, obstacles[idx].top
            
            # check for collision with hero
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.bottom = True, hero.top
                
            # check for collision with creatures
            if creatures != None:
                idx = self.rect.collidelist(creatures)            
                if idx >= 0: hitCreature, self.rect.bottom = idx, creatures[idx].top

        elif self.direction == RIGHT:
            self.rect.move_ip(self.speed, 0)
            
            # check for collision with edge of screen
            if self.rect.right >= MAX_X_2: hitEdge, self.rect.right = self.direction, MAX_X_2
            
            # check for collision with pushables
            if pushables != None:
                idx = self.rect.collidelist(pushables)
                if idx >= 0:
                    tempState.pushables[idx].rect.move_ip(self.speed, 0)
                    del pushables[idx]
                    rects = obstacles + creatures + pushables + \
                        tempState.getAvailableItemRects(visibleOnly=True)
                    idx2 = tempState.pushables[idx].rect.collidelist(rects)
                    if idx2 >= 0:
                        tempState.pushables[idx].rect.right = rects[idx2].left
                        self.rect.right = tempState.pushables[idx].rect.left
                    elif self.rect.right >= MAX_X_2 - BOXSIZE:
                        tempState.pushables[idx].rect.right = MAX_X_2
                        self.rect.right = tempState.pushables[idx].rect.left                        
                    elif tempState.pushables[idx].secretTrigger:
                        items.showSecretItem()

            # check for collision with obstacles
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.right = idx, obstacles[idx].left
            
            # check for collision with hero
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.right = True, hero.left            
                
            # check for collision with creatures
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.right = idx, creatures[idx].left
                
        elif self.direction == UP:
            self.rect.move_ip(0, -self.speed)   
            
            # check for collision with edge of screen
            if self.rect.top <= 0: hitEdge, self.rect.top = self.direction, 0
            
            # check for collision with pushables
            if pushables != None:
                idx = self.rect.collidelist(pushables)
                if idx >= 0:
                    tempState.pushables[idx].rect.move_ip(0, -self.speed)
                    del pushables[idx]
                    rects = obstacles + creatures + pushables + \
                        tempState.getAvailableItemRects(visibleOnly=True)
                    idx2 = tempState.pushables[idx].rect.collidelist(rects)
                    if idx2 >= 0:
                        tempState.pushables[idx].rect.top = rects[idx2].bottom
                        self.rect.top = tempState.pushables[idx].rect.bottom
                    elif self.rect.top < BOXSIZE:
                        tempState.pushables[idx].rect.top = 0
                        self.rect.top = tempState.pushables[idx].rect.bottom                        
                    elif tempState.pushables[idx].secretTrigger:
                        items.showSecretItem()

            # check for collision with obstacles
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.top = idx, obstacles[idx].bottom

            # check for collision with hero
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.top = True, hero.bottom            

            # check for collision with creatures
            if creatures != None:
                idx = self.rect.collidelist(creatures)
                if idx >= 0: hitCreature, self.rect.top = idx, creatures[idx].bottom

        elif self.direction == LEFT:
            self.rect.move_ip(-self.speed, 0)
            
            # check for collision with edge of screen
            if self.rect.left <= MIN_X: hitEdge, self.rect.left = self.direction, MIN_X
            
            # check for collision with pushables
            if pushables != None:
                idx = self.rect.collidelist(pushables)
                if idx >= 0:
                    tempState.pushables[idx].rect.move_ip(-self.speed, 0)
                    del pushables[idx]
                    rects = obstacles + creatures + pushables + \
                        tempState.getAvailableItemRects(visibleOnly=True)
                    idx2 = tempState.pushables[idx].rect.collidelist(rects)
                    if idx2 >= 0:
                        tempState.pushables[idx].rect.left = rects[idx2].right
                        self.rect.left = tempState.pushables[idx].rect.right
                    elif self.rect.left < BOXSIZE:
                        tempState.pushables[idx].rect.left = 0
                        self.rect.left = tempState.pushables[idx].rect.right                        
                    elif tempState.pushables[idx].secretTrigger:
                        items.showSecretItem()

            # check for collision with obstacles
            idx = self.rect.collidelist(obstacles)
            if idx >= 0: hitObstacle, self.rect.left = idx, obstacles[idx].right
            
            # check for collision with hero
            if hero != None and self.rect.colliderect(hero):
                hitHero, self.rect.left = True, hero.right
                     
            # check for collision with creatures
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
        self.heroRef = heroRef
        self.heroType = heroMap[heroRef]
        rect = Rect(tx * BOXSIZE + 3, ty * BOXSIZE + (BOXSIZE / 2), BOXSIZE - 6, BOXSIZE / 2)
        Movable.__init__(self, DOWN, tx * BOXSIZE, ty * BOXSIZE, 0, PATTERN_NONE, 0, 0, rect)
    def moving (self, direction):
        self.direction, self.speed = direction, self.heroType.speed
    def stop (self):
        self.speed = 0
    def nextHero (self):
        heroIdx = permState.unlockedHeroes.index(self.heroRef) + 1
        if heroIdx >= len(permState.unlockedHeroes): heroIdx = 0
        self.heroRef = permState.unlockedHeroes[heroIdx]        
        self.heroType = heroMap[self.heroRef]
    def prevHero (self):
        heroIdx = permState.unlockedHeroes.index(self.heroRef) - 1
        if heroIdx <= 0: heroIdx = len(permState.unlockedHeroes) - 1
        self.heroRef = permState.unlockedHeroes[heroIdx]
        self.heroType = heroMap[self.heroRef]
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

class Pushable:
    def __init__ (self, rect, featureRef, secretTrigger=False):
        self.rect, self.featureRef, self.secretTrigger = rect, featureRef, secretTrigger
