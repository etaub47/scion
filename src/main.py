import pygame, sys, anim
from pygame.locals import *

pygame.init()

DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

FPS = 25
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((768, 576))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption('Scion')

i, j = 24, 1
x, y, direction = 250, 250, DOWN
speed = 5
step = 0
ratio, anim_ratio = 0, 3
px, py = 0, 15
tx = 1
h_axis_pos, v_axis_pos = 0, 0
myJoystick = None


joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()

while True:
    DISPLAYSURF.fill((255, 255, 255))
    pressed = ""
    if myJoystick is not None:
		h_axis_pos = myJoystick.get_axis(3)
		v_axis_pos = myJoystick.get_axis(4)
		if h_axis_pos > 0.5: 
			direction = RIGHT
			speed = 5
		elif h_axis_pos < -0.5: 
			direction = LEFT
			speed = 5
		elif v_axis_pos > 0.5:
			direction = DOWN
			speed = 5
		elif v_axis_pos < -0.5: 
			direction = UP
			speed = 5
		else: speed = 0
		for b in range(0, 10):
			if myJoystick.get_button(b):
				pressed = str(b)    
    textSurf = BASICFONT.render("%s,%s -- %s" % (str(px), str(py), pressed), True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.bottomleft = 250, 250
    for r in range(0, 16):
        for s in range(0, 12):
            anim.displayTerrain(DISPLAYSURF, tx, r, s)
    anim.displaySquare(DISPLAYSURF, px, py)
    DISPLAYSURF.blit(textSurf, textRect)
    if direction == DOWN:
        y += speed
    elif direction == RIGHT:
        x += speed
    elif direction == UP:
        y -= speed
    elif direction == LEFT:
        x -= speed
    anim.displayImage(DISPLAYSURF, i, direction, step, x, y)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_o: i -= 1
            elif event.key == K_p: i += 1
            elif event.key == K_k: speed += 1
            elif event.key == K_m: speed -= 1
            elif event.key == K_LEFT: px -= 1
            elif event.key == K_RIGHT: px += 1
            elif event.key == K_UP: py -= 1
            elif event.key == K_DOWN: py += 1
            elif event.key == K_q: tx += 1
            elif event.key == K_a: tx -= 1
    pygame.display.update()
    fpsClock.tick(FPS)
    if speed > 0:
    	if ratio == anim_ratio: 
        	step += 1
    	else: 
        	ratio += 1
    if step >= 4: step = 0
