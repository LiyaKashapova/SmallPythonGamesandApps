from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, s):
        super().__init__()
        self.image = i
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
        bullet = Bullet(images['bullet'], self.rect.centerx, self.rect.top, 15)
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


images = {
    'icon': image.load('icon.png'),
    'back': transform.scale(image.load('back.png'), (1000, 700)),
    'button': image.load('button.png'),
    'buttonclicked': image.load('buttongrey.png'),
    'player': transform.scale(image.load('Shigeo.png'), (85, 170)),
    'bullet': transform.scale(image.load('lasers.png'), (30, 40)),
    'enemy': transform.scale(image.load('ghost.png'), (200, 100)),
    'bads': transform.scale(image.load('sphere.png'), (100, 100)),
    'goods': transform.scale(image.load('blast.png'), (100, 100))
}

init()
ww, wh = 1000, 700
w = display.set_mode((ww, wh))
display.set_caption('???')
display.set_icon(images['icon'])
clock = time.Clock()

mixer.init()
mixer.music.load('Mobs Theme v2.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
hit, click = mixer.Sound('hit.mp3'), mixer.Sound('click.mp3')
hit.set_volume(0.2)
click.set_volume(0.2)

font.init()
f, color = font.SysFont('Impact', 80), (154, 38, 99)
win, lose = f.render('YOU WON!', True, color), f.render('YOU LOST!', True, color)
f = font.SysFont('Impact', 40)

w.blit(images['back'], (0, 0))
w.blit(f.render('Don''t let the monsters get through!', True, color), (200, 120))
w.blit(f.render('Each                diminishes your allies''s morale', True, color), (150, 200))
w.blit(images['bads'], (250, 200))
w.blit(f.render('as well as each monsters going through you', True, color), (150, 280))
w.blit(f.render('Each                gives your allies hope, pick them up!', True, color), (120, 360))
w.blit(images['goods'], (230, 360))

button = Rect(400, 490, 210, 110)
draw.rect(w, (216, 191, 216), button, 5)
w.blit(images['button'], (405, 495))
play = f.render('Play', True, (51, 0, 102))
w.blit(play, (470, 520))


def button_click():
    click.play()
    w.blit(images['buttonclicked'], (405, 495))
    w.blit(play, (470, 520))
    display.update()
    time.delay(200)
    w.blit(images['button'], (405, 495))
    w.blit(play, (470, 520))
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


def generate():
    global monsters, bullets, bads, goods
    monsters, bullets, bads, goods = sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()
    for i in range(1, 6):
        monsters.add(Enemy(images['enemy'], randint(80, ww - 200), -40, randint(1, 3)))
    for i in range(1, 3):
        bads.add(Enemy(images['bads'], randint(30, ww - 30), -40, randint(1, 5)))
        goods.add(Enemy(images['goods'], randint(30, ww - 30), -40, randint(1, 5)))


global monsters, bullets, bads, goods
player = Player(images['player'], ww / 2, wh - 180, 15)
generate()

score = missed = fired = 0
game, reload, ctime, rtime = True, False, None, None
tcolor = color
wait, press = f.render('Wait, getting angry...', True, color), f.render('Press P to run again...', True, (245, 245, 245))
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if not game and e.key == K_p:
                game = True
                score = missed = fired = 0
                generate()
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
        w.blit(images['back'], (0, 0))
        if reload:
            ctime = timer()
            if ctime - rtime < 3:
                w.blit(wait, (360, 460))
            else:
                fired = 0
                reload = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monsters.add(Enemy(images['enemy'], randint(80, ww - 200), -40, randint(1, 5)))
        for m in monsters:
            if m.rect.y > ww:
                missed += 1
                m.rect.x = randint(80, ww - 200)
                m.rect.y = -100
        if sprite.spritecollide(player, bads, True):
            missed += 1
            bads.add(Enemy(images['bads'], randint(80, ww - 200), -40, randint(1, 5)))
        if sprite.spritecollide(player, goods, True):
            missed -= 1
            goods.add(Enemy(images['goods'], randint(80, ww - 200), -40, randint(1, 3)))
        if missed < 3:
            tcolor = color
        elif 3 < missed < 5:
            tcolor = (200, 180, 200)
        else:
            tcolor = (255, 204, 204)
        player.update()
        monsters.update()
        bads.update()
        goods.update()
        bullets.update()
        w.blit(f.render(f'Monsters: {50 - score}', True, color), (20, 20))
        if missed > 10:
            w.blit(f.render('Morale: 0', True, tcolor), (20, 100))
        else:
            w.blit(f.render(f'Morale: {10 - missed}', True, tcolor), (20, 100))
        if missed > 9:
            game = False
            w.blit(lose, (350, 300))
            w.blit(press, (320, 500))
        elif score == 50:
            game = False
            w.blit(win, (350, 300))
            w.blit(press, (320, 500))
        display.update()
        clock.tick(60)
