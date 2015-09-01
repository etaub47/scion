import os, pygame, sys, anim, state, world
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

# initialize hero
permState.hero = Hero('H1', 5, 5)

# initialize joystick
joystickCount, myJoystick = pygame.joystick.get_count(), None
h_axis_pos, v_axis_pos = 0, 0
if joystickCount > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()
    buttonsReset = True

# DEBUG
px, py = 55, 46

# load the starting screen
world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)

# main game loop
while True:

    # draw the current screen
    allDead = len(tempState.creatures) == 0
    world.drawWorld(displaySurf, permState.wx, permState.wy, permState.wz, real=True, allDead=allDead)
    anim.displayPushables(displaySurf)

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
            pressed = str(b)
            if myJoystick.get_button(b):
                
                # fire projectile
                if int(pressed) == B_BUTTON and buttonsReset:
                        buttonsReset = False
                        dir = permState.hero.direction
                        tempState.projectiles.append(Projectile(
                            'PA', dir, permState.hero.x - PROJ_OFFSET, permState.hero.y, -1))
                            
            # fire button released; ready for another shot
            elif int(pressed) == B_BUTTON:            
                buttonsReset = True
    
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
    
    # move the hero and check for collisions
    obstacles = tempState.getObstacles(True, True, False)
    pushables = tempState.getObstacles(False, False, True)
    hitResult = permState.hero.move(obstacles, None, tempState.getCreatureRects(), pushables)
    
    # check for edge of screen
    if hitResult[0] == DOWN:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.y, permState.wy = MIN_Y, permState.wy + 1
    elif hitResult[0] == RIGHT:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.x, permState.wx = MIN_X, permState.wx + 1
    elif hitResult[0] == UP:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.y, permState.wy = MAX_Y, permState.wy - 1
    elif hitResult[0] == LEFT:
        anim.scrollScreen(displaySurf, permState.hero, permState.wx, permState.wy, permState.wz)
        permState.hero.x, permState.wx = MAX_X, permState.wx - 1
    if hitResult[0] != None:
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
