from constants import *

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
        self.obstacles, self.lowObstacles, self.pushables = [], [], []
    def clear (self):
        self.projectiles[:] = []
        self.creatures[:] = []
        self.allies[:] = []
        self.obstacles[:] = []
        self.lowObstacles[:] = []
        self.pushables[:] = []
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
        
class PermanentState:
    def __init__ (self):
        self.hero = None
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
    def save (self):
        pass
    def load (self):
        pass

tempState = TemporalState()
permState = PermanentState()
