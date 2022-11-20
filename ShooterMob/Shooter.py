from pygame import *
from random import randint, uniform, choice
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
        bullet = Bullet(images['bullet'], self.rect.centerx, self.rect.top, 10)
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
    'back': transform.scale(image.load('back.jpg'), (1200, 700)),
    'button': image.load('button.png'),
    'buttonclicked': image.load('buttongrey.png'),
    'player': transform.scale(image.load('Shigeo.png'), (85, 170)),
    'bullet': transform.scale(image.load('lasers.png'), (30, 40)),
    'enemies': [transform.scale(image.load(f'enemies/e{i}.png'), (100, 100)) for i in range(1, 16)],
    'bads': transform.scale(image.load('sphere.png'), (50, 50)),
    'goods': transform.scale(image.load('blast.png'), (50, 50))
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
f, stroke, color = font.SysFont('Impact', 80), (154, 38, 99), (255, 204, 204)
win_s, win = f.render('YOU WON!', True, stroke), f.render('YOU WON!', True, color)
lose_s, lose = f.render('YOU LOST!', True, stroke), f.render('YOU LOST!', True, color)
f = font.SysFont('Impact', 40)

w.blit(images['back'], (0, 0))
w.blit(f.render('Don''t let the monsters get through!', True, stroke), (198, 118))
w.blit(f.render('Don''t let the monsters get through!', True, color), (200, 120))
w.blit(f.render('Each          diminishes your allies''s morale', True, stroke), (148, 198))
w.blit(f.render('Each          diminishes your allies''s morale', True, color), (150, 200))
w.blit(images['bads'], (235, 200))
w.blit(f.render('as well as each monsters going through you', True, stroke), (148, 278))
w.blit(f.render('as well as each monsters going through you', True, color), (150, 280))
w.blit(f.render('Each         gives your allies hope, pick them up!', True, stroke), (118, 358))
w.blit(f.render('Each         gives your allies hope, pick them up!', True, color), (120, 360))
w.blit(images['goods'], (205, 360))

button = Rect(400, 490, 210, 110)
draw.rect(w, (216, 191, 216), button, 5)
w.blit(images['button'], (405, 495))
play_s, play = f.render('Play', True, stroke), f.render('Play', True, color)
w.blit(play_s, (468, 518))
w.blit(play, (470, 520))


def button_click():
    click.play()
    w.blit(images['buttonclicked'], (405, 495))
    w.blit(play_s, (468, 518))
    w.blit(play, (470, 520))
    display.update()
    time.delay(200)
    w.blit(images['button'], (405, 495))
    w.blit(play_s, (468, 518))
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
        monsters.add(Enemy(choice(images['enemies']), randint(80, ww - 200), randint(-60, -40), uniform(1, 2)))
    for i in range(1, 3):
        bads.add(Enemy(images['bads'], randint(30, ww - 30), randint(-60, -40), uniform(1, 3)))
        goods.add(Enemy(images['goods'], randint(30, ww - 30), randint(-60, -40), uniform(1, 3)))


global monsters, bullets, bads, goods
player = Player(images['player'], ww / 2, wh - 180, 15)
generate()

score = missed = fired = 0
game, reload, ctime, rtime = True, False, None, None
wait_s, wait = f.render('Wait, getting angry...', True, stroke), f.render('Wait, getting angry...', True, color)
press_s, press = f.render('Press P to run again...', True, color), f.render('Press P to run again...', True, stroke)
tcolor = color
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
            monsters.add(Enemy(choice(images['enemies']), randint(80, ww - 200), randint(-60, -40), uniform(1, 2)))
        for m in monsters:
            if m.rect.y > ww:
                missed += 1
                m.rect.x = randint(80, ww - 200)
                m.rect.y = -100
        if sprite.spritecollide(player, bads, True):
            missed += 1
            bads.add(Enemy(images['bads'], randint(80, ww - 200), randint(-60, -40), uniform(1, 3)))
        if sprite.spritecollide(player, goods, True):
            missed -= 1
            goods.add(Enemy(images['goods'], randint(80, ww - 200), randint(-60, -40), uniform(1, 3)))
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
        w.blit(f.render(f'Monsters: {50 - score}', True, stroke), (18, 18))
        w.blit(f.render(f'Monsters: {50 - score}', True, color), (20, 20))
        if missed > 10:
            w.blit(f.render('Morale: 0', True, stroke), (18, 98))
            w.blit(f.render('Morale: 0', True, tcolor), (20, 100))
        else:
            w.blit(f.render(f'Morale: {10 - missed}', True, stroke), (18, 98))
            w.blit(f.render(f'Morale: {10 - missed}', True, tcolor), (20, 100))
        if missed > 9:
            game = False
            w.blit(lose_s, (348, 298))
            w.blit(lose, (350, 300))
            w.blit(press_s, (318, 498))
            w.blit(press, (320, 500))
        elif score == 50:
            game = False
            w.blit(win_s, (348, 298))
            w.blit(win, (350, 300))
            w.blit(press_s, (318, 498))
            w.blit(press, (320, 500))
        display.update()
        clock.tick(60)
