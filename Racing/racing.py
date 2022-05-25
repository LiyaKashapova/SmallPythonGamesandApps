import os
import random
import sys
import time as timer
from pygame import *

#  Configuration
ww = 800
wh = 600
text_c = (255, 255, 255)
back_c = (0, 0, 0)
fps = 40
min_size = 10
max_size = 40
min_speed = 2
max_speed = 8
add_rate = 6
player_speed = 5
count = 3

font.init()
f = font.SysFont('Verdana', 30)

mixer.init()
mixer.music.load('car.wav')
crash = mixer.Sound('crash.wav')
lost = mixer.Sound('laugh.wav')

car_player = image.load('car1.png')
car_spawn1 = image.load('car2.png')
car_spawn2 = image.load('car3.png')
car_spawn3 = image.load('car4.png')
player_rect = car_player.get_rect()
sample = [car_spawn2, car_spawn3, car_spawn1]
curb_left = image.load('left.png')
curb_right = image.load('right.png')


def check_hit(player, cars):
    for c in cars:
        if player.colliderect(c['rect']):
            return True
    return False


def draw_text(text, f, surface, x, y):
    textobj = f.render(text, 1, text_c)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# set up pygame, the window, and the mouse cursor
init()
mainClock = time.Clock()
w = display.set_mode((ww, wh))
display.set_caption('car race')
mouse.set_visible(False)

# "Start" screen
draw_text('Press any key to start the game.', f, w, (ww / 3) - 30, (wh / 3))
draw_text('And Enjoy', f, w, (ww / 3), (wh / 3) + 30)
display.update()

play = True
while play:
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()
        elif e.type == KEYDOWN:
            play = False

if not os.path.exists("save.dat"):
    file = open("save.dat", 'w')
    file.write(str(0))
    file.close()
v = open("save.dat", 'r')
topScore = int(v.readline())
v.close()
while count > 0:
    # start of the game
    baddies = []
    score = 0
    player_rect.topleft = (ww / 2, wh - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    mixer.music.play(-1, 0.0)

    while True:  # the game loop
        score += 1  # increase score

        for e in event.get():

            if e.type == QUIT:
                quit()
                sys.exit()

            if e.type == KEYDOWN:
                if e.key == ord('z'):
                    reverseCheat = True
                if e.key == ord('x'):
                    slowCheat = True
                if e.key == K_LEFT or e.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if e.key == K_RIGHT or e.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if e.key == K_UP or e.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if e.key == K_DOWN or e.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if e.type == KEYUP:
                if e.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if e.key == ord('x'):
                    slowCheat = False
                    score = 0
                if e.key == K_ESCAPE:
                    quit()
                    sys.exit()

                if e.key == K_LEFT or e.key == ord('a'):
                    moveLeft = False
                if e.key == K_RIGHT or e.key == ord('d'):
                    moveRight = False
                if e.key == K_UP or e.key == ord('w'):
                    moveUp = False
                if e.key == K_DOWN or e.key == ord('s'):
                    moveDown = False

        # Add new cars at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == add_rate:
            baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {'rect': Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(min_speed, max_speed),
                         'surface': transform.scale(random.choice(sample), (23, 47)),
                         }
            baddies.append(newBaddie)
            sideLeft = {'rect': Rect(0, 0, 126, 600),
                        'speed': random.randint(min_speed, max_speed),
                        'surface': transform.scale(curb_left, (126, 599)),
                        }
            baddies.append(sideLeft)
            sideRight = {'rect': Rect(497, 0, 303, 600),
                         'speed': random.randint(min_speed, max_speed),
                         'surface': transform.scale(curb_right, (303, 599)),
                         }
            baddies.append(sideRight)

        # Move the player around.
        if moveLeft and player_rect.left > 0:
            player_rect.move_ip(-1 * player_speed, 0)
        if moveRight and player_rect.right < ww:
            player_rect.move_ip(player_speed, 0)
        if moveUp and player_rect.top > 0:
            player_rect.move_ip(0, -1 * player_speed)
        if moveDown and player_rect.bottom < wh:
            player_rect.move_ip(0, player_speed)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > wh:
                baddies.remove(b)

        # Draw the game world on the window.
        w.fill(back_c)

        # Draw the score and top score.
        draw_text('Score: %s' % score, f, w, 128, 0)
        draw_text('Top Score: %s' % topScore, f, w, 128, 20)
        draw_text('Rest Life: %s' % count, f, w, 128, 40)

        w.blit(car_player, player_rect)

        for b in baddies:
            w.blit(b['surface'], b['rect'])

        display.update()

        # Check if any of the car have hit the player.
        if check_hit(player_rect, baddies):
            if score > topScore:
                g = open("data/save.dat", 'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick(fps)

    # "Game Over" screen.
    mixer.music.stop()
    count -= 1
    crash.play()
    timer.sleep(1)
    if count == 0:
        lost.play()
        draw_text('Game over', f, w, (ww / 3), (wh / 3))
        draw_text('Press any key to play again.', f, w, (ww / 3) - 80, (wh / 3) + 30)
        display.update()
        timer.sleep(2)
        while play:
            for e in event.get():
                if e.type == QUIT:
                    quit()
                    sys.exit()
                elif e.type == KEYDOWN:
                    play = False
        count = 3
        crash.stop()
