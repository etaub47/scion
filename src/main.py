import pygame, sys, anim, world
from pygame.locals import *
from pygame import Rect
from constants import *

pygame.init()

FPS = 25
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((BOXSIZE * BOARDTILEWIDTH, BOXSIZE * BOARDTILEHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption('Scion')

i, j = 'S1', 1
x, y, direction = 250, 250, DOWN
wx, wy, wz = 1, 1, 0
speed = 5
step = 0
ratio, anim_ratio = 0, 3
px, py = 55, 46
tx = 1
h_axis_pos, v_axis_pos = 0, 0
myJoystick = None

world.loadWorld(wx, wy, wz, real=True)

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()

while True:
    #DISPLAYSURF.fill((255, 255, 255))
    world.drawWorld(DISPLAYSURF, wx, wy, wz, real=True)
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
				if int(pressed) == 2:
				    anim.createProjectile('PH', direction, x, y)
    textSurf = BASICFONT.render("%s,%s -- %s" % (str(px), str(py), pressed), True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.bottomleft = 250, 250
    anim.displaySquare(DISPLAYSURF, px, py)
    DISPLAYSURF.blit(textSurf, textRect)
    rect = Rect(x + 2, y + BOXSIZE / 2, BOXSIZE - 4, BOXSIZE / 2)
    if direction == DOWN:
        if y < MAX_Y: 
            world.move(wz, wx, wy, rect, 0, speed)
            x, y = rect.x - 2, rect.y - BOXSIZE / 2 
        else: 
            anim.scrollScreen(DISPLAYSURF, i, direction, step, x, y, wx, wy, wz)
            y, wy = MIN_Y, wy + 1
            world.loadWorld(wx, wy, wz, real=True)
    elif direction == RIGHT:
        if x < MAX_X:
            world.move(wz, wx, wy, rect, speed, 0)        
            x, y = rect.x - 2, rect.y - BOXSIZE / 2
        else: 
            anim.scrollScreen(DISPLAYSURF, i, direction, step, x, y, wx, wy, wz)
            x, wx = MIN_X, wx + 1
            world.loadWorld(wx, wy, wz, real=True)
    elif direction == UP:
        if y > MIN_Y: 
            world.move(wz, wx, wy, rect, 0, -speed)
            x, y = rect.x - 2, rect.y - BOXSIZE / 2            
        else: 
            anim.scrollScreen(DISPLAYSURF, i, direction, step, x, y, wx, wy, wz)
            y, wy = MAX_Y, wy - 1
            world.loadWorld(wx, wy, wz, real=True)
    elif direction == LEFT:
        if x > MIN_X:
            world.move(wz, wx, wy, rect, -speed, 0)
            x, y = rect.x - 2, rect.y - BOXSIZE / 2            
        else: 
            anim.scrollScreen(DISPLAYSURF, i, direction, step, x, y, wx, wy, wz)
            x, wx = MAX_X, wx - 1
            world.loadWorld(wx, wy, wz, real=True)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_o: i = "S" + str(int(i[1:]) - 1)
            elif event.key == K_p: i = "S" + str(int(i[1:]) + 1)
            elif event.key == K_k: speed += 1
            elif event.key == K_m: speed -= 1
            elif event.key == K_d: px -= 1
            elif event.key == K_f: px += 1
            elif event.key == K_r: py -= 1
            elif event.key == K_c: py += 1
            elif event.key == K_LEFT: direction = LEFT
            elif event.key == K_RIGHT: direction = RIGHT
            elif event.key == K_UP: direction = UP
            elif event.key == K_DOWN: direction = DOWN
            elif event.key == K_q: tx += 1
            elif event.key == K_a: tx -= 1
            elif event.key == K_SPACE:
                anim.createProjectile('PH', direction, x, y)
    anim.displayImage(DISPLAYSURF, i, direction, step, x, y)
    anim.moveAndDisplayProjectiles(DISPLAYSURF) 
    anim.moveAndDisplayCreatures(DISPLAYSURF) 
    pygame.display.update()
    fpsClock.tick(FPS)
    if speed > 0:
    	if ratio == anim_ratio: 
        	step += 1
    	else: 
        	ratio += 1
    if step >= 4: step = 0
