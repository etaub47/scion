import pygame, anim

def loadOverworld (DISPLAYSURF, wx, wy, wz):
    if wz == 1:
        datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else:
        datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)
    with open(datafile, "r") as f:
        for cy, line in enumerate(f):
            if cy < 12:
                for cx, ckey in enumerate(line):
                    anim.displayTerrain(DISPLAYSURF, ckey, cx, cy)
            else:
                (tx, ty, tkey) = line.split(",")
                anim.displayFeature(DISPLAYSURF, tkey, int(tx), int(ty)) 

def tinyOverworld (DISPLAYSURF, wx, wy, wz, gx, gy):
    if wz == 1:
        datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else:
        datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)
    with open(datafile, "r") as f:
        for cy, line in enumerate(f):
            if cy < 12:
                for cx, ckey in enumerate(line):
                    clr = (255, 255, 255)
                    if ckey == 'A': clr = (0, 128, 0)
                    elif ckey == 'B': clr = (0, 238, 238)
                    elif ckey == 'C': clr = (139, 90, 0)
                    elif ckey == 'D': clr = (205, 179, 139)
                    elif ckey == 'E': clr = (118, 238, 0)
                    elif ckey == 'F': clr = (139, 136, 120)
                    elif ckey == 'G': clr = (139, 90, 0)
                    pygame.draw.rect(DISPLAYSURF, clr, (48 * gx + (cx * 3), 576 + (48 * gy) + (cy * 4), 3, 4), 0)
