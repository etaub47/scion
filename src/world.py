import anim

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
