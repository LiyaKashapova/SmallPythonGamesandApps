import os
from random import *
from pygame import *
import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, i, s, iw, ih, x, y):
        sprite.Sprite.__init__(self)
        self.speed = s
        self.image = transform.scale(image.load(i), (iw, ih))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Car(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.top > 0:
            self.rect.move_ip(0, -1 * self.speed)
        if keys[K_s] and self.rect.bottom < wh:
            self.rect.move_ip(0, self.speed)
        if keys[K_a] and self.rect.left > 0:
            self.rect.move_ip(-1 * self.speed, 0)
        if keys[K_d] and self.rect.right < ww:
            self.rect.move_ip(self.speed, 0)


ww, wh = 1200, 700
init()
clock = time.Clock()
w = display.set_mode((ww, wh))
display.set_caption('Traffic')
display.set_icon(transform.scale(image.load('racing.png'), (50, 50)))
mouse.set_visible(False)

stroke, back, text = (240, 240, 240), (0, 0, 0), (214, 217, 30)
font.init()
f = font.SysFont('Verdana', 30, bold=True)
mixer.init()
mixer.music.load('car.wav')
mixer.music.set_volume(0.3)
crash = mixer.Sound('crash.wav')
crash.set_volume(0.5)
lost = mixer.Sound('oh-no.mp3')

curb = {
    'left': GameSprite('curb_left.png', 0, 300, 700, 0, 0),
    'right': GameSprite('curb_right.png', 0, 300, 700, 900, 0)
}
player = Car('player.png', 5, 50, 100, ww / 2, wh - 100)
sample = ['car2.png', 'car3.png', 'car4.png']

w.blit(f.render('Press any key to start the game', True, text), ((ww / 3) - 50, (wh / 3) + 50))
display.update()
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            run = False


def save_r_w(to_do):
    global top_score
    global score
    if to_do == 'read':
        if not os.path.exists('save.dat'):
            s = open('save.dat', 'w')
            s.write(str(0))
            s.close()
        else:
            s = open('save.dat', 'r')
            top_score = int(s.readline())
            s.close()
    else:
        s = open('save.dat', 'w')
        s.write(str(score))
        s.close()
        top_score = score


def check_hit(cs):
    global player
    global curb
    r = player.rect
    if r.colliderect(curb['left'].rect) or r.colliderect(curb['right'].rect):
        return True
    if sprite.spritecollide(player, cs, True):
        return True
    return False


cars = sprite.Group()
score, top_score, add_rate, lives = 0, 0, 0, 3
save_r_w('read')
mixer.music.play(-1)
run = game = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif not game and e.type == KEYDOWN:
            game = True
            save_r_w('read')
            for c in cars:
                c.kill()
            mixer.music.play(-1)
            score, add_rate, lives = 0, 0, 3
    if game:
        w.fill(back)
        curb['left'].draw()
        curb['right'].draw()
        score += 1
        add_rate += 1
        if add_rate == 20:
            add_rate = 0
            cars.add(GameSprite(choice(sample), randint(2, 8), 50, 100, randint(300, 850), -50))
        for c in cars:
            c.rect.move_ip(0, randint(2, 8))
            if c.rect.top > wh:
                cars.remove(c)
        cars.draw(w)
        player.move()
        player.draw()
        w.blit(f.render('Score: %s' % score, True, back), (8, 8))
        w.blit(f.render('Score: %s' % score, True, text), (10, 10))
        w.blit(f.render('Top Score: %s' % top_score, True, back), (8, 58))
        w.blit(f.render('Top Score: %s' % top_score, True, text), (10, 60))
        w.blit(f.render('Lives: %s' % lives, True, back), (8, 108))
        w.blit(f.render('Lives: %s' % lives, True, text), (10, 110))
        clock.tick(40)
        display.update()
        if check_hit(cars):
            lives -= 1
            player.rect.x = ww / 2
            player.rect.y = wh - 100
            for c in cars:
                c.kill()
            mixer.music.stop()
            crash.play()
            timer.sleep(1)
            crash.stop()
            mixer.music.play(-1)
        if lives == 0:
            mixer.music.stop()
            lost.play()
            w.blit(f.render('Game over', True, back), ((ww / 3) + 118, (wh / 3) + 50))
            w.blit(f.render('Game over', True, text), ((ww / 3) + 120, (wh / 3) + 50))
            w.blit(f.render('Press any key to play again', True, back), ((ww / 3) - 32, (wh / 3) + 150))
            w.blit(f.render('Press any key to play again', True, text), ((ww / 3) - 30, (wh / 3) + 150))
            if score > top_score:
                save_r_w('')
            game = False
            display.update()
            timer.sleep(3)
