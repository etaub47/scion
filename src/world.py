import anim

def loadOverworld (DISPLAYSURF, wx, wy):
	datafile = "../data/world_%02d_%02d.dat" % (wx, wy)
	with open(datafile, "r") as f:
		for cy, line in enumerate(f):
			if cy < 12:
				for cx, ckey in enumerate(line):
					anim.displayTerrain(DISPLAYSURF, ckey, cx, cy)
			else:
				(tx, ty, tkey) = line.split(",")
				anim.displayFeature(DISPLAYSURF, tkey, int(tx), int(ty)) 
				
