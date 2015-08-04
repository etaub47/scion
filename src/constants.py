BOXSIZE = 48
BOARDTILEWIDTH = 16
BOARDTILEHEIGHT = 12
BOARDWIDTH = BOARDTILEWIDTH * BOXSIZE
BOARDHEIGHT = BOARDTILEHEIGHT * BOXSIZE

MIN_X = 0 - (BOXSIZE / 4)
MIN_Y = 0 - (BOXSIZE / 4)
MAX_X = (BOXSIZE * BOARDTILEWIDTH) - BOXSIZE + (BOXSIZE / 4)
MAX_Y = (BOXSIZE * BOARDTILEHEIGHT) - BOXSIZE + (BOXSIZE / 4)

WORLD_MAX_X = 8
WORLD_MAX_Y = 8
DUNGEON_MAX_X = 4
DUNGEON_MAX_Y = 4
DUNGEON_MAX_Z = 4

WHITE = (255, 255, 255)
BRIGHTYELLOW = (255, 255, 0)
OFFWHITE = (255, 250, 205)
GRAY = (90, 90, 90)

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

SOURCE_IDX = 0

SPRITE_IDX = 0
DIR_IDX = 1
X_IDX = 2
Y_IDX = 3
SPEED_IDX = 4
PATTERN_IDX = 5
STEP_IDX = 6
TIMER_IDX = 7
RECT_IDX = 8