from constants import *
from pygame import Rect

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
        self.obstacles, self.lowObstacles, self.pushables = [], [], []
        self.availableItems = [] # AvailableItem
        self.stairs, self.checkForStairs = None, False
        self.doors = [] # (x, y, doorState, rect, number)
    def clear (self):
        self.projectiles[:] = []
        self.creatures[:] = []
        self.allies[:] = []
        self.obstacles[:] = []
        self.lowObstacles[:] = []
        self.pushables[:] = []
        self.availableItems[:] = []
        self.stairs, self.checkForStairs = None, False
        self.doors[:] = []
    def getCreatureRects (self, itself = -1):
        creatureRects = []
        for idx, creature in enumerate(self.creatures):
            if idx != itself:
                creatureRects.append(creature.rect)
        return creatureRects
    def getObstacles (self, returnObstacles, returnLowObstacles, returnPushables, returnLockedDoors=True):
        retValue = []
        if returnObstacles: 
            retValue += self.obstacles
            for door in self.doors:
                if (not door.isOpen()) and (returnLockedDoors or not door.isLocked()): 
                    retValue.append(door.rect)
        if returnLowObstacles: retValue += self.lowObstacles
        if returnPushables: 
            for pushable in self.pushables: 
                retValue.append(pushable.rect)
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
        
class PermanentState:
    def __init__ (self):
        self.hero, self.heroIdx = None, -1
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
        self.obtainedItems = [] # unique items already obtained
        # DEBUG: currently unlock all heroes for testing purposes
        self.unlockedHeroes = ['H1', 'H2', 'H4', 'H5', 'H6', 'H8', 'H17'] # heroes unlocked
        self.unlockedDoors = [] # locked doors already opened (wx, wy, wz, x, y)
        self.keys = 1
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
