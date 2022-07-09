from pygame import *
from random import randint, choice
import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, iw, ih, s):
        super().__init__()
        self.image = transform.scale(i, (iw, ih))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def draw(self, s):
        s.blit(self.image, (self.rect.x, self.rect.y))


ww = 1200
wh = 700
w = display.set_mode((ww, wh))
display.set_caption('Hunger!')
display.set_icon(transform.scale(image.load('icon.png'), (50, 50)))
mouse.set_visible(False)
clock = time.Clock()

images = {
    'back': transform.scale(image.load('back.jpg'), (ww, wh)),
    'gems': [image.load(f'Gems/{i}.png') for i in range(1, 22)],
    'stones': [image.load(f'Stones/{i}.png') for i in range(1, 16)],
    'alien': image.load('alien.png'),
    'plate': image.load('plate.png')
}

font.init()
f = font.SysFont('Verdana', 50, bold=True, italic=True)
t_stroke = (255, 255, 255)
t_color = (25, 0, 50)

mixer.init()
mixer.music.load('main.mp3')
mixer.music.set_volume(0.3)
gulp = mixer.Sound('gulp.mp3')
sigh = mixer.Sound('sigh.mp3')
end = mixer.Sound('end.mp3')

run = play = True
mixer.music.play(-1)
while run and play:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            play = False
    w.blit(images['back'], (0, 0))
    w.blit(f.render("On a distant planet,", True, t_stroke), (118, 50 - 2))
    w.blit(f.render("On a distant planet,", True, t_color), (120, 50))
    w.blit(f.render("an alien is trying to eat!", True, t_stroke), (298, 150 - 2))
    w.blit(f.render("an alien is trying to eat!", True, t_color), (300, 150))
    w.blit(f.render("Help him and catch gems by", True, t_stroke), (118, 300 - 2))
    w.blit(f.render("Help him and catch gems by", True, t_color), (120, 300))
    w.blit(f.render("sliding left 'a' and right 'd'", True, t_stroke), (298, 400 - 2))
    w.blit(f.render("sliding left 'a' and right 'd'", True, t_color), (300, 400))
    w.blit(f.render("Press any key to start the game...", True, t_stroke), (118, 550 - 2))
    w.blit(f.render("Press any key to start the game...", True, t_color), (120, 550))
    display.update()
    clock.tick(60)

alien = GameSprite(images['alien'], ww / 2 - 100, wh - 300, 200, 300, 10)
plate = GameSprite(images['plate'], ww / 2 - 75, wh - 140, 150, 45, 10)
gems = sprite.Group()
stones = sprite.Group()
tick = int(timer.time())
generation = score = die = 0
play = True
mr = ml = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if play:
                if e.key == K_a:
                    ml = True
                elif e.key == K_d:
                    mr = True
            else:
                generation = score = die = 0
                tick = int(timer.time())
                end.stop()
                mixer.music.play(-1)
                for g in gems:
                    gems.remove(g)
                for s in stones:
                    stones.remove(s)
                play = True
        elif e.type == KEYUP:
            if e.key == K_a:
                ml = False
            elif e.key == K_d:
                mr = False
    if play:
        if mr:
            if alien.rect.x >= ww:
                alien.rect.x = 0
                plate.rect.x = 25
            else:
                alien.rect.x += alien.speed
                plate.rect.x += alien.speed
        elif ml:
            if alien.rect.x <= 0:
                alien.rect.x = ww - alien.image.get_width()
                plate.rect.x = ww - alien.image.get_width() + 25
            else:
                alien.rect.x -= alien.speed
                plate.rect.x -= alien.speed
        cur_time = int(timer.time())
        if cur_time - tick == 1:
            generation += 1
            die += 1
            tick = cur_time
        if generation == 3:
            generation += 1
            gems.add([GameSprite(choice(images['gems']), randint(50, ww - 50), randint(-300, -50), 50, 50, 0) for i in range(7)])
        elif generation == 5:
            generation = 0
            stones.add(
                [GameSprite(choice(images['stones']), randint(50, ww - 50), randint(-300, -50), 50, 50, 0) for i in range(3)])
        for g in gems:
            g.rect.y += randint(1, 5)
            if g.rect.y > wh:
                gems.remove(g)
        for s in stones:
            s.rect.y += randint(1, 3)
            if s.rect.y > wh:
                stones.remove(s)
        if sprite.spritecollide(plate, gems, True):
            gulp.play()
            score += 1
            if score % 3 == 0:
                die = 0
        if sprite.spritecollide(plate, stones, True):
            score = 0
            die += 3
        w.blit(images['back'], (0, 0))
        if 50 - score == 0:
            w.blit(f.render(f'Hooray!', True, t_stroke), (ww / 2 - 100, 180))
            w.blit(f.render(f'Hooray!', True, t_color), (ww / 2 - 100, 182))
            w.blit(f.render(f'Now our friend can sleep)', True, t_stroke), (ww / 2 - 320, 280))
            w.blit(f.render(f'Now our friend can sleep)', True, t_color), (ww / 2 - 320, 282))
            alien.rect.x = ww / 2 - 100
            plate.rect.x = ww / 2 - 75
            alien.draw(w)
            w.blit(f.render(f'Press any key to play again...', True, t_stroke), (118, wh - 100))
            w.blit(f.render(f'Press any key to play again...', True, t_color), (120, wh - 102))
            display.update()
            end.play(-1)
            timer.sleep(10)
            play = False
        elif 10 - die <= 0:
            w.blit(f.render(f'Oh, no! Our friend...', True, t_stroke), (ww / 2 - 250, 180))
            w.blit(f.render(f'Oh, no! Our friend...', True, t_color), (ww / 2 - 250, 182))
            w.blit(f.render(f'DIED of hunger', True, t_stroke), (ww / 2 - 210, 280))
            w.blit(f.render(f'DIED of hunger', True, t_color), (ww / 2 - 210, 282))
            alien.rect.x = ww / 2 - 100
            plate.rect.x = ww / 2 - 75
            alien.draw(w)
            w.blit(f.render(f'Press any key to try again...', True, t_stroke), (118, wh - 100))
            w.blit(f.render(f'Press any key to try again...', True, t_color), (120, wh - 102))
            display.update()
            sigh.play()
            timer.sleep(5)
            play = False
        else:
            w.blit(f.render(f'Need to be staffed: {50 - score}', True, t_stroke), (20, 20))
            w.blit(f.render(f'Need to be staffed: {50 - score}', True, t_color), (20, 22))
            w.blit(f.render(f'Dying from hunger: {10 - die}', True, t_stroke), (20, 100))
            w.blit(f.render(f'Dying from hunger: {10 - die}', True, t_color), (20, 102))
            alien.draw(w)
            plate.draw(w)
            gems.draw(w)
            stones.draw(w)
        display.update()
        clock.tick(60)