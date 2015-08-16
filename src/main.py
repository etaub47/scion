import os, pygame, sys, anim, world
from pygame.locals import *
from pygame import Rect
from constants import *
from movables import *
from state import tempState, permState

# initialize all imported pygame modules
pygame.init()

# initialize clock, display surface, font, and caption
fpsClock = pygame.time.Clock()
displaySurf = pygame.display.set_mode((BOXSIZE * BOARDTILEWIDTH, BOXSIZE * BOARDTILEHEIGHT))
basicFont = pygame.font.Font('freesansbold.ttf', 20)
displaySurf.fill((255, 255, 255))
pygame.display.set_caption('Scion')

# initialize joystick
joystickCount, myJoystick = pygame.joystick.get_count(), None
if joystickCount > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()
    h_axis_pos, v_axis_pos = 0, 0

# DEBUG
px, py = 55, 46

# load the starting screen
world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)

# main game loop
while True:

    # draw the current screen
    world.drawWorld(displaySurf, permState.wx, permState.wy, permState.wz, real=True)

    # process keyboard input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
        
            # DEBUG
            if event.key == K_o: i = "S" + str(int(i[1:]) - 1)
            elif event.key == K_p: i = "S" + str(int(i[1:]) + 1)
            elif event.key == K_k: speed += 1            
            elif event.key == K_m: speed -= 1
            elif event.key == K_d: px -= 1
            elif event.key == K_f: px += 1
            elif event.key == K_r: py -= 1
            elif event.key == K_c: py += 1
            
            # fire projectile
            elif event.key == K_SPACE:                
                tempState.projectiles.append(Projectile(
                    'PA', permState.hero.direction, permState.hero.x - PROJ_OFFSET, permState.hero.y, -1))
                    
    # process joystick input
    pressed = ""
    if myJoystick is not None:
        h_axis_pos = myJoystick.get_axis(3)
        v_axis_pos = myJoystick.get_axis(4)
        for b in range(0, 10):
            if myJoystick.get_button(b):
                pressed = str(b)
                
                # fire projectile
                if int(pressed) == B_BUTTON:
                    tempState.projectiles.append(Projectile(
                        'PA', permState.hero.direction, permState.hero.x - PROJ_OFFSET, permState.hero.y, -1))
    
    # check hero movement
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or h_axis_pos < -0.5: permState.hero.moving(LEFT)
    elif keys[K_RIGHT] or h_axis_pos > 0.5: permState.hero.moving(RIGHT)
    elif keys[K_UP] or v_axis_pos < -0.5: permState.hero.moving(UP)
    elif keys[K_DOWN] or v_axis_pos > 0.5: permState.hero.moving(DOWN)
    else: permState.hero.stop()
            
    # DEBUG
    textSurf = basicFont.render("%s,%s -- %s" % (str(px), str(py), pressed), True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.bottomleft = 250, 250
    anim.displaySquare(displaySurf, px, py)
    displaySurf.blit(textSurf, textRect)
    
    # move the hero and check for collisions and edge of screen    
    hitResult = permState.hero.move(world.getObstacles(), None, tempState.getCreatureRects())
    if permState.hero.direction == DOWN and hitResult[0]:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.y, permState.wy = MIN_Y, permState.wy + 1
    elif permState.hero.direction == RIGHT and hitResult[0]:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.x, permState.wx = MIN_X, permState.wx + 1
    elif permState.hero.direction == UP and hitResult[0]:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.y, permState.wy = MAX_Y, permState.wy - 1
    elif permState.hero.direction == LEFT and hitResult[0]:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.x, permState.wx = MAX_X, permState.wx - 1
    if hitResult[0]: 
        world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)
        permState.hero.updateRect()
    
    # update the other movables and redraw the screen
    anim.displayHero(displaySurf, permState.hero)
    anim.moveAndDisplayProjectiles(displaySurf, permState.wz, permState.wx, permState.wy) 
    anim.moveAndDisplayCreatures(displaySurf, permState.wz, permState.wx, permState.wy)
    anim.displayLifeMeter(displaySurf, 3)    
    pygame.display.update()
    fpsClock.tick(FPS)
    if permState.hero.speed > 0: permState.hero.tick()
