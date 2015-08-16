from constants import *
from movables import *

class TemporalState:
    def __init__ (self):
        self.projectiles, self.creatures, self.allies = [], [], []
    def clear (self):
        self.projectiles[:] = []
        self.creatures[:] = []
        self.allies[:] = []
    def getCreatureRects (self, itself = -1):
        creatureRects = []
        for idx, creature in enumerate(self.creatures):
            if idx != itself:
                creatureRects.append(creature.rect)
        return creatureRects
        
class PermanentState:
    def __init__ (self):
        self.hero = Hero('H1', 5, 5)
        self.wx, self.wy, self.wz = START_WX, START_WY, START_WZ
    def save (self):
        pass
    def load (self):
        pass
        
tempState = TemporalState()
permState = PermanentState()
