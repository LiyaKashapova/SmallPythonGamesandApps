from random import randint
from pygame import *
from time import time as timer
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, w, h, s):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(i), (w, h))
        self.speed = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < ww - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(resource_path('lasers.png'), self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wh:
            self.rect.x = randint(80, ww - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ww = 1000
wh = 700

w = display.set_mode((ww, wh))
display.set_caption('???')
display.set_icon(image.load(resource_path('icon.png')))
back = transform.scale(image.load(resource_path('back.png')), (ww, wh))

mixer.init()
mixer.music.load(resource_path('Mobs Theme v2.mp3'))
mixer.music.set_volume(0.1)
mixer.music.play()
hit = mixer.Sound(resource_path('hit.mp3'))
hit.set_volume(0.2)
click = mixer.Sound(resource_path('click.mp3'))
click.set_volume(0.2)

w.blit(back, (0, 0))
font.init()
f = font.SysFont('Impact', 80)
win = f.render('YOU WON!', True, (154, 38, 99))
lose = f.render('YOU LOST!', True, (154, 38, 99))
f = font.SysFont('Impact', 40)

press = f.render('Press P to play again...', True, (245, 245, 245))
w.blit(f.render('Don''t let the monsters get through!', True, (154, 38, 99)), (200, 120))
w.blit(f.render('Each                diminishes your allies''s morale', True, (154, 38, 99)), (150, 200))
w.blit(transform.scale(image.load(resource_path('sphere.png')), (60, 50)), (250, 200))
w.blit(f.render('as well as each monsters going through you', True, (154, 38, 99)), (150, 280))
w.blit(f.render('Each                gives your allies hope, pick them up!', True, (154, 38, 99)), (120, 360))
w.blit(transform.scale(image.load(resource_path('blast.png')), (50, 50)), (230, 360))
button = Rect(400, 490, 210, 110)
draw.rect(w, (216, 191, 216), button, 5)
b = image.load(resource_path('button.png'))
bg = image.load(resource_path('buttongrey.png'))
w.blit(b, (405, 495))
w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))


def button_click():
    global game
    click.play()
    w.blit(bg, (405, 495))
    w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))
    display.update()
    time.delay(200)
    w.blit(b, (405, 495))
    w.blit(f.render('Play', True, (51, 0, 102)), (470, 520))
    display.update()
    game = False


run = game = True
while run and game:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if button.collidepoint(x, y): button_click()
        display.update()

reload = False
score = lost = fire = 0
color = (154, 38, 99)
player = Player(resource_path('Shigeo.png'), ww / 2, wh - 180, 85, 170, 15)
monsters = sprite.Group()
for i in range(1, 6):
    monsters.add(Enemy(resource_path('ghost.png'), randint(80, ww - 200), -40, 200, 100, randint(1, 5)))
obs = sprite.Group()
blasts = sprite.Group()
for i in range(1, 3):
    obs.add(Enemy(resource_path('sphere.png'), randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
    blasts.add(Enemy(resource_path('blast.png'), randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
bullets = sprite.Group()

game = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if not game and e.key == K_p:
                game = True
                score = lost = fire = 0
                for b in bullets: b.kill()
                for m in monsters: m.kill()
                for o in obs: o.kill()
                for b in blasts: b.kill()
                for i in range(1, 6):
                    monsters.add(Enemy(resource_path('ghost.png'), randint(80, ww - 200), -40, 200, 100, randint(1, 5)))
                for i in range(1, 3):
                    obs.add(Enemy(resource_path('sphere.png'), randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
                    blasts.add(Enemy(resource_path('blast.png'), randint(30, ww - 30), -40, 100, 100, randint(1, 7)))
            if e.key == K_SPACE:
                if fire < 10 and not reload:
                    fire += 1
                    hit.play()
                    player.fire()
                if fire > 9 and not reload:
                    ltime = timer()
                    reload = True
    if game:
        w.blit(back, (0, 0))
        if reload:
            ntime = timer()
            if ntime - ltime < 3:
                w.blit(f.render('Wait, getting angry...', True, (154, 38, 99)), (360, 460))
            else:
                fire = 0
                reload = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monsters.add(Enemy(resource_path('ghost.png'), randint(80, ww - 200), -100, 200, 100, randint(1, 5)))
        for m in monsters:
            if m.rect.y > ww:
                lost -= 1
                m.rect.x = randint(80, ww - 200)
                m.rect.y = -100
        if sprite.spritecollide(player, blasts, True):
            lost -= 1
            blasts.add(Enemy(resource_path('blast.png'), randint(80, ww - 200), -40, 100, 100, randint(1, 5)))
        if sprite.spritecollide(player, obs, True):
            lost += 1
        if 3 > lost:
            color = (154, 38, 99)
        if 5 > lost > 1:
            color = (216, 191, 216)
        if 8 > lost > 5:
            color = (255, 204, 204)
        w.blit(f.render('Monsters: ' + str(50 - score), True, (154, 38, 99)), (20, 20))
        w.blit(f.render('Morale: ' + str(10 - lost), True, color), (20, 100))
        player.update()
        monsters.update()
        obs.update()
        blasts.update()
        bullets.update()
        player.reset()
        monsters.draw(w)
        obs.draw(w)
        blasts.draw(w)
        bullets.draw(w)
        if lost == 10:
            game = False
            w.blit(lose, (350, 300))
            w.blit(press, (320, 500))
        elif score == 50:
            game = False
            w.blit(win, (350, 300))
            w.blit(press, (320, 500))
        display.update()
