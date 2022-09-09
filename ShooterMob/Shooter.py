from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, w, h, s):
        super().__init__()
        self.image = transform.scale(image.load(i), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < ww - 80:
            self.rect.x += self.speed
        self.draw()

    def fire(self):
        bullet = Bullet('lasers.png', self.rect.centerx, self.rect.top, 30, 40, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > wh:
            self.rect.x = randint(80, ww - 80)
            self.rect.y = 0
            missed += 1
        self.draw()


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        self.draw()
        if self.rect.y < 0:
            self.kill()


init()
ww, wh = 1000, 700
w = display.set_mode((ww, wh))
display.set_caption('???')
display.set_icon(image.load('icon.png'))
back = transform.scale(image.load('back.png'), (ww, wh))

mixer.init()
mixer.music.load('Mobs Theme v2.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
hit = mixer.Sound('hit.mp3')
hit.set_volume(0.2)
click = mixer.Sound('click.mp3')
click.set_volume(0.2)

font.init()
f = font.SysFont('Impact', 80)
win = f.render('YOU WON!', True, (154, 38, 99))
lose = f.render('YOU LOST!', True, (154, 38, 99))
f = font.SysFont('Impact', 40)

w.blit(back, (0, 0))
w.blit(f.render('Don''t let the monsters get through!', True, (154, 38, 99)), (200, 120))
w.blit(f.render('Each                diminishes your allies''s morale', True, (154, 38, 99)), (150, 200))
w.blit(transform.scale(image.load('sphere.png'), (60, 50)), (250, 200))
w.blit(f.render('as well as each monsters going through you', True, (154, 38, 99)), (150, 280))
w.blit(f.render('Each                gives your allies hope, pick them up!', True, (154, 38, 99)), (120, 360))
w.blit(transform.scale(image.load('blast.png'), (50, 50)), (230, 360))

button = Rect(400, 490, 210, 110)
draw.rect(w, (216, 191, 216), button, 5)
b, bg = image.load('button.png'), image.load('buttongrey.png')
w.blit(b, (405, 495))
w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))


def button_click():
    click.play()
    w.blit(bg, (405, 495))
    w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))
    display.update()
    time.delay(200)
    w.blit(b, (405, 495))
    w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))
    display.update()
    global game
    game = False


run = game = True
while run and game:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if button.collidepoint(e.pos):
                button_click()
        display.update()

player = Player('Shigeo.png', ww / 2, wh - 180, 85, 170, 15)
monsters = sprite.Group()
for i in range(1, 6):
    monsters.add(Enemy('ghost.png', randint(80, ww - 200), -40, 200, 100, randint(1, 5)))
spheres = sprite.Group()
blasts = sprite.Group()
for i in range(1, 3):
    spheres.add(Enemy('sphere.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
    blasts.add(Enemy('blast.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
bullets = sprite.Group()
obs = sprite.Group()
blasts = sprite.Group()
for i in range(1, 3):
    obs.add(Enemy('sphere.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
    blasts.add(Enemy('blast.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
bullets = sprite.Group()

score = missed = fired = 0
game = True
reload = False
color = (154, 38, 99)
press = f.render('Press P to run again...', True, (245, 245, 245))
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if not game and e.key == K_p:
                game = True
                score = missed = fired = 0
                for b in bullets: b.kill()
                for m in monsters: m.kill()
                for o in obs: o.kill()
                for b in blasts: b.kill()
                for i in range(1, 6):
                    monsters.add(Enemy('ghost.png', randint(80, ww - 200), -40, 200, 100, randint(1, 5)))
                for i in range(1, 3):
                    obs.add(Enemy('sphere.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
                    blasts.add(Enemy('blast.png', randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
            if e.key == K_SPACE:
                if not reload:
                    if fired < 9:
                        fired += 1
                        hit.play()
                        player.fire()
                    else:
                        rtime = timer()
                        reload = True
    if game:
        w.blit(back, (0, 0))
        if reload:
            ctime = timer()
            if ctime - rtime < 3:
                w.blit(f.render('Wait, getting angry...', True, (154, 38, 99)), (360, 460))
            else:
                fired = 0
                reload = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monsters.add(Enemy('ghost.png', randint(80, ww - 200), -100, 200, 100, randint(1, 5)))
        for m in monsters:
            if m.rect.y > ww:
                missed -= 1
                m.rect.x = randint(80, ww - 200)
                m.rect.y = -100
        if sprite.spritecollide(player, blasts, True):
            missed -= 1
            blasts.add(Enemy('blast.png', randint(80, ww - 200), -40, 100, 100, randint(1, 5)))
        if sprite.spritecollide(player, obs, True):
            missed += 1
        if missed < 3:
            color = (154, 38, 99)
        elif 3 < missed < 5:
            color = (216, 191, 216)
        else:
            color = (255, 204, 204)
        player.update()
        monsters.update()
        spheres.update()
        blasts.update()
        bullets.update()
        w.blit(f.render('Monsters: ' + str(50 - score), True, (154, 38, 99)), (20, 20))
        if missed > 10:
            w.blit(f.render('Morale: 0', True, (154, 38, 99)), (20, 100))
        else:
            w.blit(f.render('Morale: ' + str(10 - missed), True, (154, 38, 99)), (20, 100))
        if missed > 9:
            game = False
            w.blit(lose, (350, 300))
            w.blit(press, (320, 500))
        elif score == 50:
            game = False
            w.blit(win, (350, 300))
            w.blit(press, (320, 500))
        display.update()
