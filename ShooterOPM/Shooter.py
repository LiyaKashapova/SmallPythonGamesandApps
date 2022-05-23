from random import randint
from pygame import *
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
        bullet = Bullet(resource_path('punch.png'), self.rect.centerx, self.rect.top, 30, 40, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wh:
            self.rect.x = randint(80, ww-80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


score = lost = 0
ww = 1000
wh = 700

w = display.set_mode((ww, wh))
display.set_caption('Saitama vs BlackSperm')
display.set_icon(image.load(resource_path('icon.png')))
back = transform.scale(image.load(resource_path('back.png')), (ww, wh))
player = Player(resource_path('Saitama.png'), ww/2, wh-180, 85, 170, 15)
monsters = sprite.Group()
for i in range(1, 6):
    monsters.add(Enemy(resource_path('BlackSperm.png'), randint(80, ww-80), -40, 40, 100, randint(1, 5)))
bullets = sprite.Group()
font.init()
f = font.SysFont('Impact', 80)
win = f.render('YOU WON!', True, (180, 0, 0))
lose = f.render('YOU LOST!', True, (180, 0, 0))
f = font.SysFont('Impact', 40)

mixer.init()
mixer.music.load(resource_path('Seigi Shikkou.mp3'))
mixer.music.set_volume(0.1)
mixer.music.play()
hit = mixer.Sound(resource_path('hit.mp3'))
hit.set_volume(0.2)

run = game = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hit.play()
                player.fire()
    if game:
        w.blit(back, (0, 0))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monsters.add(Enemy(resource_path('BlackSperm.png'), randint(80, ww-80), -40, 40, 100, randint(1, 5)))
        if lost >= 5:
            game = False
            w.blit(lose, (350, 300))
        elif score == 100:
            game = False
            w.blit(win, (350, 300))
        w.blit(f.render('Score: ' + str(score), True, (180, 0, 0)), (20, 20))
        w.blit(f.render('Missed: ' + str(lost), True, (180, 0, 0)), (20, 80))
        player.update()
        monsters.update()
        bullets.update()
        player.reset()
        monsters.draw(w)
        bullets.draw(w)
        display.update()
        time.delay(30)