from constants import *

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
        self.obstacles, self.lowObstacles, self.pushables = [], [], []
        self.availableItems = []
        self.allDead = False
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
    def getAvailableItemRects (self, visibleOnly=False):
        rects = []
        for availableItem in self.availableItems:
            if not visibleOnly or availableItem.showState == VISIBLE:
                rects.append(availableItem.rect)
        return rects
    def deleteAvailableItem (self, idx):
        self.availableItems[idx].showState = COLLECTED
        
class PermanentState:
    def __init__ (self):
        self.hero, self.heroIdx = None, -1
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
        self.obtainedItems = [] # unique items already obtained
        self.unlockedHeroes = ['H1', 'H2', 'H4', 'H5', 'H6', 'H8', 'H17']
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
