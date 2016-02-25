import os, pygame, sys, anim, state, graphics, items, world
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
tempState.hero = Hero('H1', START_X, START_Y, permState.maxHp, permState.maxAttack, permState.maxDefense)

# initialize joystick
joystickCount, myJoystick = pygame.joystick.get_count(), None
h_axis_pos, v_axis_pos = 0, 0
if joystickCount > 0:
    myJoystick = pygame.joystick.Joystick(0)
    myJoystick.init()
    buttonsReset = [True] * MAX_BUTTONS

# DEBUG
px, py = 55, 46

# load the starting screen
world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)

# main game loop
while True:

    # draw the current background
    world.drawTerrain(displaySurf, permState.wx, permState.wy, permState.wz, real=True)
    graphics.displayStairs(displaySurf)

    # process keyboard input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
        
            # DEBUG
            if event.key == K_o: i = "S" + str(int(i[1:]) - 1)
            elif event.key == K_p: i = "S" + str(int(i[1:]) + 1)
            elif event.key == K_d: px -= 1
            elif event.key == K_f: px += 1
            elif event.key == K_r: py -= 1
            elif event.key == K_c: py += 1
            
            # fire projectile
            elif event.key == K_SPACE:                
                tempState.projectiles.append(Projectile(
                    'PA', tempState.hero.direction, tempState.hero.x - PROJ_OFFSET, tempState.hero.y, -1))
                    
    # process joystick input
    pressed = ""
    if myJoystick is not None:
        h_axis_pos = myJoystick.get_axis(3)
        v_axis_pos = myJoystick.get_axis(4)
        for b in range(0, 10):
            pressed = str(b)
            if myJoystick.get_button(b):
                
                # fire projectile
                if int(pressed) == B_BUTTON and buttonsReset[B_BUTTON]:
                    buttonsReset[B_BUTTON] = False
                    dir = tempState.hero.direction
                    tempState.projectiles.append(Projectile('PA', dir, tempState.hero.x, tempState.hero.y, -1))
                        
                # change hero
                elif int(pressed) == R_BUTTON and buttonsReset[R_BUTTON]:
                    buttonsReset[R_BUTTON] = False
                    tempState.hero.nextHero()
                elif int(pressed) == L_BUTTON and buttonsReset[L_BUTTON]:
                    buttonsReset[L_BUTTON] = False
                    tempState.hero.prevHero()
                                                                    
            # button released; ready to press again
            elif int(pressed) == B_BUTTON:            
                buttonsReset[B_BUTTON] = True
            elif int(pressed) == R_BUTTON:
                buttonsReset[R_BUTTON] = True
            elif int(pressed) == L_BUTTON:
                buttonsReset[L_BUTTON] = True
    
    # check hero movement
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] or h_axis_pos < -0.5: tempState.hero.moving(LEFT)
    elif keys[K_RIGHT] or h_axis_pos > 0.5: tempState.hero.moving(RIGHT)
    elif keys[K_UP] or v_axis_pos < -0.5: tempState.hero.moving(UP)
    elif keys[K_DOWN] or v_axis_pos > 0.5: tempState.hero.moving(DOWN)
    else: tempState.hero.stop()
            
    # DEBUG
    textSurf = basicFont.render("%s,%s -- %s" % (str(px), str(py), pressed), True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.bottomleft = 250, 250
    anim.displaySquare(displaySurf, px, py)
    displaySurf.blit(textSurf, textRect)
    
    # check for locked doors that can be opened
    if permState.keys > 0:
        idx = tempState.hero.rect.collidelist(tempState.getLockedDoorRects())
        if idx >= 0: items.unlockDoor(idx)
    
    # check for collisions
    filter = INCLUDE_OBSTACLES
    if permState.keys == 0: filter = filter | INCLUDE_LOCKED_DOORS
    if not tempState.gotWings: filter = filter | INCLUDE_WATER_OBSTACLES | INCLUDE_POISON_OBSTACLES
    obstacles = tempState.getObstacles(filter)    
    pushables = tempState.getObstacles(INCLUDE_PUSHABLES)
    hitResult = tempState.hero.move(obstacles, None, tempState.getCreatureRects(), pushables)
    
    # check for item collection
    idx = tempState.hero.rect.collidelist(tempState.getAvailableItemRects())
    if idx >= 0: items.getItem(idx)
    
    # check for edge of screen
    if hitResult[HIT_EDGE] == DOWN:
        anim.scrollScreen(displaySurf, tempState.hero, permState.wx, permState.wy, permState.wz)
        tempState.hero.y, permState.wy = MIN_Y, permState.wy + 1
    elif hitResult[HIT_EDGE] == RIGHT:
        anim.scrollScreen(displaySurf, tempState.hero, permState.wx, permState.wy, permState.wz)
        tempState.hero.x, permState.wx = MIN_X, permState.wx + 1
    elif hitResult[HIT_EDGE] == UP:
        anim.scrollScreen(displaySurf, tempState.hero, permState.wx, permState.wy, permState.wz)
        tempState.hero.y, permState.wy = MAX_Y, permState.wy - 1
    elif hitResult[HIT_EDGE] == LEFT:
        anim.scrollScreen(displaySurf, tempState.hero, permState.wx, permState.wy, permState.wz)
        tempState.hero.x, permState.wx = MAX_X, permState.wx - 1
    if hitResult[HIT_EDGE] != None:
        world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)
        tempState.hero.updateRect()
        
    # check for staircase
    if tempState.stairs != None and tempState.hero.rect.colliderect(tempState.stairs[3]):
        if tempState.checkForStairs:    
            if permState.wz > 0:
                s_idx, s_idx2 = permState.wz - 1, 0
            else:
                s_idx, s_idx2 = ord(tempState.stairs[4][1]) - 70, 1
            permState.wz, permState.wx, permState.wy = STAIRS[s_idx][s_idx2]
            world.loadWorld(permState.wx, permState.wy, permState.wz, real=True)
            tempState.hero.x, tempState.hero.y = tempState.stairs[0] * BOXSIZE, \
                tempState.stairs[1] * BOXSIZE
            tempState.hero.updateRect()
    else:
        tempState.checkForStairs = True
        
    # check for collision with creature (damage)
    if hitResult[HIT_CREATURE] != None:
        creature = tempState.creatures[hitResult[HIT_CREATURE]]
        tempState.hero.hp -= 1 # TODO: this should be dependent on the creature
        # TODO: temporary invincibility
        if tempState.hero.hp <= 0:
            tempState.hero.hp = 0 # TODO: and of course death
    
    # update the other movables
    anim.moveCreatures(displaySurf)
    anim.moveProjectiles(displaySurf) 

    # redraw the screen
    graphics.redrawScreen(displaySurf)
    graphics.drawHeadsUpDisplay(displaySurf)
    pygame.display.update()
    
    # update the clocks
    fpsClock.tick(FPS)
    if tempState.hero.speed > 0: tempState.hero.tick()
    tempState.incrementTimer()
