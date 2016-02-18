from constants import *
from pygame import Rect

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
        self.obstacles, self.waterObstacles, self.clearObstacles = [], [], []
        self.fakeObstacles, self.fakeWaterObstacles, self.pushables = [], [], []
        self.poisonObstacles, self.fakePoisonObstacles = [], []
        self.availableItems = [] # AvailableItem
        self.stairs, self.checkForStairs, self.gotMirror, self.gotWings = None, False, False, False
        self.doors = [] # (x, y, doorState, rect, number)
        self.timer = 0
    def clear (self):
        self.projectiles[:], self.creatures[:], self.allies = [], [], []
        self.obstacles[:], self.waterObstacles[:], self.clearObstacles[:] = [], [], []
        self.fakeObstacles[:], self.fakeWaterObstacles[:], self.pushables[:] = [], [], []
        self.poisonObstacles[:], self.fakePoisonObstacles[:] = [], []
        self.availableItems[:] = []
        self.stairs, self.checkForStairs, self.gotMirror, self.gotWings = None, False, False, False
        self.doors[:] = []
        self.timer = 0
    def getCreatureRects (self, itself = -1):
        creatureRects = []
        for idx, creature in enumerate(self.creatures):
            if idx != itself:
                creatureRects.append(creature.rect)
        return creatureRects
    def getObstacles (self, filter):
        retValue = []
        if filter & INCLUDE_OBSTACLES > 0: 
            retValue += self.obstacles
            for door in self.doors: 
                if not door.isOpen() and not door.isLocked(): retValue.append(door.rect)
        if filter & INCLUDE_WATER_OBSTACLES > 0: retValue += self.waterObstacles
        if filter & INCLUDE_PUSHABLES > 0: 
            for pushable in self.pushables: retValue.append(pushable.rect)
        if filter & INCLUDE_FAKE_OBSTACLES > 0: retValue += self.fakeObstacles
        if filter & INCLUDE_FAKE_WATER_OBSTACLES > 0: retValue += self.fakeWaterObstacles
        if filter & INCLUDE_LOCKED_DOORS > 0: 
            for door in self.doors: 
                if door.isLocked(): retValue.append(door.rect)
        if filter & INCLUDE_CLEAR_OBSTACLES: retValue += self.clearObstacles
        if filter & INCLUDE_POISON_OBSTACLES > 0: retValue += self.poisonObstacles
        if filter & INCLUDE_FAKE_POISON_OBSTACLES > 0: retValue += self.fakePoisonObstacles
        return retValue
    def getLockedDoorRects (self):
        rects = []
        for door in self.doors:
            if door.isLocked():
                rects.append(door.rect)
            else:
                # this hack keeps the locked door indexes aligned with the door indexes in tempState
                rects.append(Rect(9999, 9999, 9, 9))
        return rects        
    def getAvailableItemRects (self, visibleOnly=False):
        rects = []
        for availableItem in self.availableItems:
            if not visibleOnly or availableItem.showState == VISIBLE:
                rects.append(availableItem.rect)
        return rects
    def deleteAvailableItem (self, idx):
        # this "deletes" an available item without modifying the collection
        # this is done to preserve the item indexes in the collection
        self.availableItems[idx].showState = COLLECTED
    def incrementTimer (self):
        self.timer += 1
        if self.timer == 100:
            self.timer = 0
        
class PermanentState:
    def __init__ (self):
        self.hero, self.heroIdx = None, -1
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
        self.obtainedItems = [] # unique items already obtained
        # DEBUG: currently unlock all heroes for testing purposes
        self.unlockedHeroes = ['H1', 'H2', 'H4', 'H5', 'H6', 'H8', 'H17'] # heroes unlocked
        self.unlockedDoors = [] # locked doors already opened as a list of tuples (wx, wy, wz, x, y)
        # DEBUG: start out with a key
        self.keys = 1
        self.life = 3
    def alreadyObtained (self, wz, wx, wy, x, y):
        return (wz, wx, wy, x, y) in self.obtainedItems
    def obtain (self, x, y):
        self.obtainedItems.append((self.wz, self.wx, self.wy, x, y))
    def save (self):
        pass
    def load (self):
        pass

tempState = TemporalState()
permState = PermanentState()
