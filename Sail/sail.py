from pygame import *
from random import randint, uniform, choice
import math as m
import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, s):
        super().__init__()
        self.image = i
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def draw(self, s):
        s.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    trail = []
    start = None

    def draw(self, s):
        x, y = mouse.get_pos()
        angle = m.degrees(m.atan2(-(y - self.rect.centery), x - self.rect.centerx)) - 90
        rot_player = transform.rotate(self.image, angle)
        for t in self.trail:
            if timer.time() - t.start > 1: self.trail.remove(t)
            else: s.blit(t.image, (t.rect.x, t.rect.y))
        s.blit(rot_player, rot_player.get_rect(center=self.rect.center))

    def update(self, s):
        x, y = mouse.get_pos()
        d = Vector2(x - self.rect.x, y - self.rect.y)
        if d != Vector2():
            d.normalize()
            d.scale_to_length(self.speed)
            self.rect.move_ip(d)
            if not self.start or timer.time() - self.start > 0.3:
                blup.play()
                self.start = timer.time()
                t = GameSprite(images['trail'], randint(self.rect.centerx - 5, self.rect.centerx + 5),
                               randint(self.rect.bottom - 20, self.rect.bottom + 20), 0)
                t.start = timer.time()
                self.trail.append(t)


class Obs(GameSprite):
    def update(self, s, o):
        self.rect.y += self.speed
        if self.rect.y > s.get_height():
            self.kill()
            o.add(Obs(choice(images['obs']), randint(10, ww - 10), -10, uniform(1, 3)))
        else:
            self.draw(s)


class Fish(GameSprite):
    def update(self, s, f, i):
        self.rect.x += self.speed
        if i == 'left' and self.rect.x > s.get_width():
            self.kill()
            f.add(Fish(choice(images['fish']), randint(-30, -10), randint(50, wh - 300), uniform(1, 3)))
        elif i == 'right' and self.rect.x < 0:
            self.kill()
            f.add(Fish(transform.flip(choice(images['fish']), True, False), randint(ww + 10, ww + 30), randint(50, wh - 300), uniform(-3, -1)))
        else:
            self.draw(s)


init()
ww, wh = 1200, 700
w = display.set_mode((ww, wh))
display.set_caption('Sail')
display.set_icon(image.load('icon.png'))
clock = time.Clock()

images = {
    'back': transform.scale(image.load('back.jpg'), (ww, wh)),
    'octo': transform.scale(image.load('octo.png'), (150, 170)),
    'trail': transform.scale(image.load('trail.png'), (50, 50)),
    'heart': transform.scale(image.load('heart.png'), (50, 50)),
    'silhouette': transform.scale(image.load('silhouette.png'), (50, 50)),
    'obs': [transform.scale(image.load(f'Anchors/{i}.png'), (50, 100)) for i in range(1, 10)] +
           [transform.scale(image.load(f'Stones/{i}.png'), (50, 50)) for i in range(1, 16)],
    'fish': [transform.scale(image.load(f'Fish/{i}.png'), (100, 50)) for i in range(1, 17)]
}

stroke, text = (10, 10, 10), (120, 0, 150)
font.init()
f = font.SysFont('Century', 50, bold=True)
win = [f.render('Good job! You made It)', True, stroke), f.render('Good job! You made It)', True, text)]
lose = [f.render('You have to be more carefull!', True, stroke), f.render('You have to be more carefull!', True, text)]
press = [f.render('Press P to play again...', True, stroke), f.render('Press P to play again...', True, text)]

mixer.init()
mixer.music.load('canon.mp3')
mixer.music.set_volume(0.4)
mixer.music.play(-1)
hit, blup, caught = mixer.Sound('hit.mp3'), mixer.Sound('bubbles.mp3'), mixer.Sound('catch.mp3')
blup.set_volume(0.6)

player = Player(images['octo'], ww / 2, wh / 2, 3)
obs, fish_left, fish_right = sprite.Group(), sprite.Group(), sprite.Group()
for i in range(1, 5): obs.add(Obs(choice(images['obs']), randint(10, ww - 10), -10, uniform(1, 3)))
for i in range(1, 3):
    fish_left.add(Fish(choice(images['fish']), randint(-30, -10), randint(50, wh - 300), uniform(1, 3)))
    fish_right.add(Fish(transform.flip(choice(images['fish']), True, False), randint(ww + 10, ww + 30), randint(50, wh - 300), uniform(-3, -1)))

run = play = True
move = False
lives, catch = 3, 50
while run:
    for e in event.get():
        if e.type == QUIT: run = False
        elif e.type == MOUSEBUTTONDOWN: move = True
        elif e.type == MOUSEBUTTONUP: move = False
        elif e.type == KEYDOWN:
            if not play and e.key == K_p:
                play, move, lives, catch = True, False, 3, 50
                player.rect.x = w.get_width() / 2
                player.rect.y = w.get_height() / 2
                for o in obs: o.kill()
                for l in fish_left: l.kill()
                for r in fish_right: r.kill()
                for i in range(1, 5): obs.add(Obs(choice(images['obs']), randint(10, ww - 10), -10, uniform(1, 3)))
                for i in range(1, 3):
                    fish_left.add(Fish(choice(images['fish']), randint(-30, -10), randint(50, wh - 300), uniform(1, 3)))
                    fish_right.add(Fish(transform.flip(choice(images['fish']), True, False), randint(ww + 10, ww + 30), randint(50, wh - 300), uniform(-3, -1)))
    if play:
        if move: player.update(w)
        w.blit(images['back'], (0, 0))
        player.draw(w)
        obs.update(w, obs)
        fish_left.update(w, fish_left, 'left')
        fish_right.update(w, fish_right, 'right')
        if sprite.spritecollide(player, fish_left, True):
            caught.play()
            catch -= 1
            fish_left.add(Fish(choice(images['fish']), randint(-30, -10), randint(50, wh - 300), uniform(1, 3)))
        elif sprite.spritecollide(player, fish_right, True):
            caught.play()
            catch -= 1
            fish_right.add(Fish(transform.flip(choice(images['fish']), True, False), randint(ww + 10, ww + 30), randint(50, wh - 300), uniform(-3, -1)))
        elif sprite.spritecollide(player, obs, True):
            hit.play()
            lives -= 1
            obs.add(Obs(choice(images['obs']), randint(10, ww - 10), -10, uniform(1, 3)))
        for i in range(0, lives): w.blit(images['heart'], (20 + (10 + images['heart'].get_width()) * i, 20))
        w.blit(images['silhouette'], (20, 80))
        w.blit(f.render(f': {catch}', True, text), (27 + images['silhouette'].get_width(), 75))
        w.blit(f.render(f': {catch}', True, stroke), (30 + images['silhouette'].get_width(), 75))
        if lives < 1:
            play = False
            w.blit(lose[0], (245, 300))
            w.blit(lose[1], (250, 300))
            w.blit(press[0], (315, 500))
            w.blit(press[1], (320, 500))
        elif catch == 0:
            play = False
            w.blit(win[0], (315, 300))
            w.blit(win[1], (320, 300))
            w.blit(press[0], (315, 500))
            w.blit(press[1], (320, 500))
    display.update()
    clock.tick(60)