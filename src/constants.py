BOXSIZE = 48
BOARDTILEWIDTH = 16
BOARDTILEHEIGHT = 12
BOARDWIDTH = BOARDTILEWIDTH * BOXSIZE
BOARDHEIGHT = BOARDTILEHEIGHT * BOXSIZE
PROJ_OFFSET = 7

FPS = 25

MIN_X = 0 - (BOXSIZE / 4)
MIN_Y = 0 - (BOXSIZE / 4)
MAX_X = (BOXSIZE * BOARDTILEWIDTH) - BOXSIZE + (BOXSIZE / 4)
MAX_Y = (BOXSIZE * BOARDTILEHEIGHT) - BOXSIZE + (BOXSIZE / 4)

WORLD_MAX_X, WORLD_MAX_Y = 8, 8
DUNGEON_MAX_X, DUNGEON_MAX_Y, DUNGEON_MAX_Z = 4, 4, 4

WHITE = (255, 255, 255)
BRIGHTYELLOW = (255, 255, 0)
OFFWHITE = (255, 250, 205)
GRAY = (90, 90, 90)

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3
HERO, ENEMY = 0, 1
PATTERN_RANDOM, PATTERN_STRAIGHT, PATTERN_NONE = 0, 1, 2

START_WX, START_WY, START_WZ = 2, 2, 0

X_BUTTON = 0
A_BUTTON = 1
B_BUTTON = 2
Y_BUTTON = 3
L_BUTTON = 4
R_BUTTON = 5

TYPE_CLEAR = 1
TYPE_OBSTACLE = 2
TYPE_LOW = 3
TYPE_PUSHABLE = 4
TYPE_ITEM = 5
TYPE_ADDITION = 6
TYPE_NUMBER = 7
TYPE_STAIRS = 8
