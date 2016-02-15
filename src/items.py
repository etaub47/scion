from constants import *
from state import tempState, permState
from pygame import Rect

UNIQUE_ITEM = 1
NORMAL_ITEM = 2

class ItemType:
    def __init__ (self, id, type, cost, duration, effect):
        self.id, self.type, self.cost, self.duration, self.effect = id, type, cost, duration, effect
        
itemMap = {
    'IA': ItemType('IA', NORMAL_ITEM, 0, 0, 0), # wings (fly over low obstacles)
    'IB': ItemType('IB', UNIQUE_ITEM, 0, 0, 0), # armor (permanent defense)
    'IC': ItemType('IC', UNIQUE_ITEM, 0, 0, 0), # book (permanent max hp)
    'ID': ItemType('ID', NORMAL_ITEM, 0, 0, 0), # shield (temporary defense)
    'IE': ItemType('IE', NORMAL_ITEM, 0, 0, 0), # meat (+HP a little)
    'IF': ItemType('IF', UNIQUE_ITEM, 0, 0, 0), # gold (+GP a little)
    'IG': ItemType('IG', NORMAL_ITEM, 0, 0, 0), # potion (+HP a lot)
    'IH': ItemType('IH', NORMAL_ITEM, 0, 0, 0), # bracelet
    'II': ItemType('II', NORMAL_ITEM, 0, 0, 0), # staff (destroys all creatures on screen)
    'IJ': ItemType('IJ', UNIQUE_ITEM, 0, 0, 0), # sword (permanent offense)
    'IK': ItemType('IK', UNIQUE_ITEM, 0, 0, 0), # chest (+GP a lot)
    'IL': ItemType('IL', UNIQUE_ITEM, 0, 0, 0), # key (+KEYS)
    'IM': ItemType('IM', NORMAL_ITEM, 0, 0, 0), # glove (temporary offense)
    'IN': ItemType('IN', NORMAL_ITEM, 0, 0, 0), # boots (temporary speed)
    'IO': ItemType('IO', NORMAL_ITEM, 0, 0, 0), # cloak (temporary invincibility)
    'IP': ItemType('IP', NORMAL_ITEM, 0, 0, 0), # amulet
    'IQ': ItemType('IQ', NORMAL_ITEM, 0, 0, 0), # mirror (see illusions)
    'IR': ItemType('IR', UNIQUE_ITEM, 0, 0, 0), # lantern (see in dark dungeons)
    'IS': ItemType('IS', NORMAL_ITEM, 0, 0, 0)  # ring
}

class AvailableItem:
    def __init__ (self, itemTypeRef, x, y, showState=VISIBLE):
        self.itemType, self.x, self.y, self.showState = itemMap[itemTypeRef], x, y, showState
        self.rect = Rect(x * BOXSIZE, y * BOXSIZE, BOXSIZE, BOXSIZE)
        
class Door:
    def __init__ (self, x, y, showState, number):
        self.x, self.y, self.showState, self.number = x, y, showState, number
        self.rect = Rect(x * BOXSIZE, y * BOXSIZE, BOXSIZE, BOXSIZE)
    def isOpen (self):
        return self.showState == OPEN
    def isLocked (self):
        return self.showState == AFTER_KEY

def getItem (idx):
    # called when the player picks up an available item
    item = tempState.availableItems[idx]
    # only visible items may be picked up
    if item.showState != VISIBLE: return
    # this item is no longer available
    tempState.deleteAvailableItem(idx)
    # if this is a unique item, mark item as no longer available
    if item.itemType.type == UNIQUE_ITEM: permState.obtain(item.x, item.y)
    # key
    if item.itemType.id == 'IL': permState.keys += 1
    # mirror
    elif item.itemType.id == 'IQ': tempState.gotMirror = True
    # wings
    elif item.itemType.id == 'IA': tempState.gotWings = True
    
def unlockDoor (idx):
    # called when the player bumps into a locked door and has a key
    door = tempState.doors[idx]
    door.showState = OPEN
    permState.unlockedDoors.append((permState.wx, permState.wy, permState.wz, door.x, door.y))
    permState.keys -= 1

def showHiddenItems ():
    # show items that only appear after all enemies on the screen are defeated
    for availableItem in tempState.availableItems:
        if availableItem.showState == AFTER_VICTORY and \
                not permState.alreadyObtained(permState.wz, permState.wx, 
                permState.wy, availableItem.x, availableItem.y):
            availableItem.showState = VISIBLE
    # open doors that remain closed until all enemies on the screen are defeated
    # permanently unlock them too
    for door in tempState.doors:
        if door.showState == AFTER_VICTORY:
            door.showState = OPEN
            permState.unlockedDoors.append((permState.wx, permState.wy, permState.wz, door.x, door.y))
        
def showSecretItem ():
    # show the item that only appears after the room secret is triggered
    for availableItem in tempState.availableItems:
        if availableItem.showState == AFTER_SECRET and \
                not permState.alreadyObtained(permState.wz, permState.wx, 
                permState.wy, availableItem.x, availableItem.y):
            availableItem.showState = VISIBLE
    # open doors that remain closed until the room secret is triggered
    # permanently unlock them too
    for door in tempState.doors:
        if door.showState == AFTER_SECRET:
            door.showState = OPEN
            permState.unlockedDoors.append((permState.wx, permState.wy, permState.wz, door.x, door.y))
    
