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
MAX_X_2 = (BOXSIZE * BOARDTILEWIDTH) + (BOXSIZE / 4)
MAX_Y_2 = (BOXSIZE * BOARDTILEHEIGHT) + (BOXSIZE / 4)

WORLD_MAX_X, WORLD_MAX_Y = 8, 8
DUNGEON_MAX_X, DUNGEON_MAX_Y, DUNGEON_MAX_Z = 4, 4, 4

WHITE = (255, 255, 255)
BRIGHTYELLOW = (255, 255, 0)
OFFWHITE = (255, 250, 205)
GRAY = (90, 90, 90)

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3
HERO, ENEMY = 0, 1
PATTERN_RANDOM, PATTERN_STRAIGHT, PATTERN_NONE = 0, 1, 2

START_WX, START_WY, START_WZ = 7, 1, 0
START_X, START_Y = 9, 5

MOVE_WALK = 1
MOVE_SWIM = 2
MOVE_FLY = 3

X_BUTTON = 0
A_BUTTON = 1
B_BUTTON = 2
Y_BUTTON = 3
L_BUTTON = 4
R_BUTTON = 5
MAX_BUTTONS = 6

TYPE_CLEAR = 1
TYPE_OBSTACLE = 2
TYPE_LOW = 3
TYPE_PUSHABLE = 4
TYPE_ITEM = 5
TYPE_ADDITION = 6
TYPE_NUMBER = 7
TYPE_STAIRS = 8
TYPE_DOOR = 9

VISIBLE = 1
OPEN = 1
AFTER_VICTORY = 2
AFTER_SECRET = 3
COLLECTED = 4 # items only
AFTER_KEY = 5 # doors only

DOOR_OPEN = 1
DOOR_AFTER_VICTORY = 2
DOOR_SECRET = 3
DOOR_NEEDS_KEY = 4

STAIRS = (((0, 2, 1), (1, 2, 4)), ((0, 4, 3), (2, 1, 1)), ((0, 8, 8), (3, 1, 1)), ((0, 8, 2), (4, 1, 1)))