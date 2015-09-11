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

def getItem (idx):
    # called when the player picks up an available item
    item = tempState.availableItems[idx]
    tempState.deleteAvailableItem(idx) # this item is no longer available
    # if this is a unique item, mark item as no longer available
    if item.itemType.type == UNIQUE_ITEM:
        permState.obtain(item.x, item.y)

def showHiddenItems ():
    # show items that only appear after all enemies on the screen are defeated
    for availableItem in tempState.availableItems:
        if availableItem.showState == AFTER_VICTORY and \
                not permState.alreadyObtained(permState.wz, permState.wx, 
                permState.wy, availableItem.x, availableItem.y):
            availableItem.showState = VISIBLE

def showSecretItem ():
    # show the item that only appears after the room secret is triggered
    for availableItem in tempState.availableItems:
        if availableItem.showState == AFTER_SECRET and \
                not permState.alreadyObtained(permState.wz, permState.wx, 
                permState.wy, availableItem.x, availableItem.y):
            availableItem.showState = VISIBLE
