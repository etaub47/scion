import pygame, sys, anim, world
from pygame.locals import *
from pygame import Rect
from constants import *
from movables import *

pygame.init()

FPS = 25
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((BOXSIZE * BOARDTILEWIDTH, BOXSIZE * BOARDTILEHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF.fill((255, 255, 255))
pygame.display.set_caption('Scion')

wx, wy, wz = 6, 5, 0
px, py = 55, 46
tx = 1
h_axis_pos, v_axis_pos = 0, 0
myJoystick = None
hero = Hero('H1', 5, 5)

world.loadWorld(wx, wy, wz, real=True)

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()

while True:

    world.drawWorld(DISPLAYSURF, wx, wy, wz, real=True)

    pressed = ""    
    if myJoystick is not None:
		h_axis_pos = myJoystick.get_axis(3)
		v_axis_pos = myJoystick.get_axis(4)
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
    
    obstacles = world.getObstacles()
    hitResult = hero.move(obstacles, None, None) # TODO: hero, creatures
    if hero.direction == DOWN and hitResult[0]:
        anim.scrollScreen(DISPLAYSURF, hero, wx, wy, wz)
        hero.y, wy = MIN_Y, wy + 1
    elif hero.direction == RIGHT and hitResult[0]:
        anim.scrollScreen(DISPLAYSURF, hero, wx, wy, wz)
        hero.x, wx = MIN_X, wx + 1
    elif hero.direction == UP and hitResult[0]:
        anim.scrollScreen(DISPLAYSURF, hero, wx, wy, wz)
        hero.y, wy = MAX_Y, wy - 1
    elif hero.direction == LEFT and hitResult[0]:
        anim.scrollScreen(DISPLAYSURF, hero, wx, wy, wz)
        hero.x, wx = MAX_X, wx - 1
    if hitResult[0]: 
        world.loadWorld(wx, wy, wz, real=True)
        hero.updateRect()
        
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
            elif event.key == K_q: tx += 1
            elif event.key == K_a: tx -= 1
            elif event.key == K_SPACE:
                anim.createProjectile('PA', hero.direction, hero.x, hero.y)
            
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or h_axis_pos < -0.5: hero.moving(LEFT)
    elif keys[K_RIGHT] or h_axis_pos > 0.5: hero.moving(RIGHT)
    elif keys[K_UP] or v_axis_pos < -0.5: hero.moving(UP)
    elif keys[K_DOWN] or v_axis_pos > 0.5: hero.moving(DOWN)
    else: hero.stop()
    
    anim.displayHero(DISPLAYSURF, hero, hero.x, hero.y)
    anim.moveAndDisplayProjectiles(DISPLAYSURF, wz, wx, wy) 
    anim.moveAndDisplayCreatures(DISPLAYSURF, wz, wx, wy)
    anim.displayLifeMeter(DISPLAYSURF, 3)    
    pygame.display.update()
    fpsClock.tick(FPS)
    if hero.speed > 0: hero.tick()
