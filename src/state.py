from constants import *

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
        self.obstacles, self.lowObstacles, self.pushables = [], [], []
        self.availableItems = []
    def clear (self):
        self.projectiles[:] = []
        self.creatures[:] = []
        self.allies[:] = []
        self.obstacles[:] = []
        self.lowObstacles[:] = []
        self.pushables[:] = []
        self.availableItems[:] = []
    def getCreatureRects (self, itself = -1):
        creatureRects = []
        for idx, creature in enumerate(self.creatures):
            if idx != itself:
                creatureRects.append(creature.rect)
        return creatureRects
    def getObstacles (self, returnObstacles, returnLowObstacles, returnPushables):
        retValue = []
        if returnObstacles: retValue += self.obstacles
        if returnLowObstacles: retValue += self.lowObstacles
        if returnPushables: 
            for pushable in self.pushables: 
                retValue.append(pushable.rect)
        return retValue
    def getAvailableItemRects (self):
        return list(map((lambda x: x.rect), self.availableItems))
    def deleteAvailableItem (self, item):
        self.availableItems.remove(item)
        
class PermanentState:
    def __init__ (self):
        self.hero = None
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
        self.obtainedItems = [] # unique items already obtained
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
