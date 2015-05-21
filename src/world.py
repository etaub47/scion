import pygame, anim

terrain = [[[[[0 for x in range(12)] for x in range(16)] for x in range(3)] for x in range(3)] for x in range(5)]
features = {}

def loadFile (wx, wy, wz):
    if wz == 0: datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
    else: datafile = "../data/dungeon%d_%02d_%02d.dat" % (wz, wx, wy)    
    with open(datafile, "r") as f:
        for cy, line in enumerate(f):
            if cy < 12:
                for cx, ckey in enumerate(line):
                    terrain[wz][wx][wy][cx - 1][cy - 1] = ckey
            else:
                (tx, ty, tkey) = line.split(",")
                features[(wz, wx, wy, int(tx), int(ty))] = tkey

def loadWorld (wx, wy, wz):
    for roomx in range(wx - 1, wx + 2):
        for roomy in range(wy - 1, wy + 2):
            if roomx > 0 and roomy > 0:
                loadFile(roomx, roomy, wz)
                
def drawWorld (DISPLAYSURF, wx, wy, wz):
    for x in range(16):
        for y in range(12):
            anim.displayTerrain(DISPLAYSURF, terrain[wz][wx][wy][x][y], x, y)
    for feature in features:            
        anim.displayFeature(DISPLAYSURF, features[feature], x, y)

def tinyOverworld (DISPLAYSURF, wx, wy, wz):
    for gx in range(wx - 1, wx + 2):
        for gy in range(wy - 1, wy + 2):
            if gx > 0 and gy > 0:
                for x in range(16):
                    for y in range(12):
                        ckey = terrain[wz][wx][wy][x][y]
                        clr = (255, 255, 255)
                        if ckey == 'A': clr = (0, 128, 0)
                        elif ckey == 'B': clr = (0, 238, 238)
                        elif ckey == 'C': clr = (139, 90, 0)
                        elif ckey == 'D': clr = (205, 179, 139)
                        elif ckey == 'E': clr = (118, 238, 0)
                        elif ckey == 'F': clr = (139, 136, 120)
                        elif ckey == 'G': clr = (139, 90, 0)
                        pygame.draw.rect(DISPLAYSURF, clr, (48 * gx + (x * 3), 576 + (48 * gy) + (y * 4), 3, 4), 0)
