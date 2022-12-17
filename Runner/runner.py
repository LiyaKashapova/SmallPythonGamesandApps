from pygame import *
from random import randint
import time as timer


class Runner(sprite.Sprite):
    state = 'idle'  # idle, run, jump, fall, slide, cheer
    frame = rate = 0

    def __init__(self):
        sprite.Sprite.__init__(self)
        self.i_idle = image.load("Player/idle.png")
        self.i_jump = image.load("Player/jump.png")
        self.i_fall = image.load("Player/fall.png")
        self.i_slide = image.load("Player/slide.png")
        self.i_run = [image.load("Player/run1.png"), image.load("Player/run2.png"), image.load("Player/run3.png")]
        self.i_cheer = [image.load("Player/cheer1.png"), image.load("Player/cheer2.png")]
        self.image = self.i_idle
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, wh - self.rect.height - 100

    def run(self):
        if self.rate == 5:
            self.frame += 1
            self.rate = 0
        if self.frame == 3:
            self.frame = 0
        self.rate += 1
        self.rect.y = wh - self.rect.height - 100
        self.image = self.i_run[self.frame]

    def jump(self):
        if self.rect.y < wh - self.rect.height - 400:
            self.state = 'fall'
        else:
            self.image = self.i_jump
            self.rect.y -= 30

    def fall(self):
        if self.rect.y >= wh - self.rect.height - 100:
            self.state = 'run'
        else:
            self.image = self.i_fall
            self.rect.y += 25

    def slide(self):
        self.image = self.i_slide
        self.rect.y = wh - self.rect.height - 50

    def cheer(self):
        if self.rate == 7:
            self.rate = 0
            if self.frame == 0:
                self.frame = 1
            else:
                self.frame = 0
            self.rect.y = wh - self.rect.height - 100
            self.image = self.i_cheer[self.frame]
        self.rate += 1

    def update(self):
        if self.state == 'idle':
            self.image = self.i_idle
        elif self.state == 'run':
            self.run()
        elif self.state == 'jump':
            self.jump()
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'slide':
            self.slide()
        else:
            self.cheer()
        c = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = c
        w.blit(self.image, (self.rect.x, self.rect.y))


class Obstacle(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load('boulder.png'), (200, 100))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(ww + 200, ww + 600), randint(300, 700)
        self.speed = 25

    def update(self):
        if self.rect.x < -200:
            self.rect.x, self.rect.y = randint(ww + 200, ww + 600), randint(300, 700)
        self.rect.x -= self.speed
        w.blit(self.image, (self.rect.x, self.rect.y))


class Monster(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load('ghost.png'), (700, 600))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -50, 100

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Torch(sprite.Sprite):
    frame = rate = 0

    def __init__(self, x):
        sprite.Sprite.__init__(self)
        self.frames = []
        for n in range(1, 8):
            self.frames.append(transform.scale(image.load('Torch/torch%s.png' % n), (50, 200)))
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, 150)

    def update(self):
        self.image = self.frames[self.frame]
        if self.frame == 6:
            self.frame = 0
        if self.rate == 2:
            self.frame += 1
            self.rate = 0
        self.rate += 1
        if self.rect.x < -50:
            self.rect.center = (self.rect.x + 1250, 150)
        else:
            self.rect.x -= 5


init()
ww, wh = 1200, 800
w = display.set_mode((ww, wh))
display.set_caption('Run for your life!')
display.set_icon(transform.scale(image.load('icon.png'), (50, 50)))
mouse.set_visible(False)
back = transform.scale(image.load('back.png'), (ww, wh))
clock = time.Clock()

font.init()
f = font.SysFont('Verdana', 50, bold=True, italic=True)
stroke, color = (255, 255, 255), (0, 115, 0)
lost = [f.render("You were knocked down!", True, stroke), f.render("You were knocked down!", True, color),
        f.render("Press any key to try again...", True, stroke), f.render("Press any key to try again...", True, color)]
won = [f.render("The ghost disappeared!", True, stroke), f.render("The ghost disappeared!", True, color), ]

mixer.init()
main_s = mixer.Sound('main.mp3')
main_s.set_volume(0.15)
main_s.play(-1)
running = mixer.Channel(1)
run_s, jump_s, slide_s, end_s = mixer.Sound('run.mp3'), mixer.Sound('jump.mp3'), mixer.Sound('slide.mp3'), mixer.Sound('end.mp3')
end_s.set_volume(0.2)

player = Runner()
torches = sprite.Group(Torch(150), Torch(450), Torch(750), Torch(1050))
run = play = True
while run and play:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            player.state = 'run'
            running.play(run_s, -1)
            play = False
    w.blit(back, (0, 0))
    torches.draw(w)
    w.blit(f.render("Don't get hit by the blocks,", True, stroke), (120 - 2, 50 - 2))
    w.blit(f.render("Don't get hit by the blocks,", True, color), (120, 50))
    w.blit(f.render("while running from ghost!", True, stroke), (300 - 2, 150 - 2))
    w.blit(f.render("while running from ghost!", True, color), (300, 150))
    w.blit(f.render("Press 'w' to jump, press 's' to slide", True, stroke), (120 - 2, 300 - 2))
    w.blit(f.render("Press 'w' to jump, press 's' to slide", True, color), (120, 300))
    w.blit(f.render("Press any key to start the game...", True, stroke), (200 - 2, 400 - 2))
    w.blit(f.render("Press any key to start the game...", True, color), (200, 400))
    player.update()
    display.update()
    clock.tick(60)

ghost = Monster()
obs = sprite.Group()
obs_rate = 0
play = True
start = timer.time()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if play:
                if e.key == K_w:
                    running.stop()
                    jump_s.play()
                    player.state = 'jump'
                elif e.key == K_s:
                    running.stop()
                    slide_s.play()
                    player.state = 'slide'
            else:
                for o in obs:
                    o.kill()
                obs_rate = 0
                start = timer.time()
                play = True
    if play:
        if player.state == 'run' and not running.get_busy():
            running.play(run_s, -1)
        obs_rate += 1
        if obs_rate == 5:
            obs.add(Obstacle())
        w.blit(back, (0, 0))
        torches.update()
        torches.draw(w)
        ghost.draw()
        obs.update()
        player.update()
        if sprite.spritecollide(player, obs, False):
            w.blit(lost[0], (300 - 2, 200 - 2))
            w.blit(lost[1], (300, 200))
            w.blit(lost[2], (300 - 2, 400 - 2))
            w.blit(lost[3], (300, 400))
            running.stop()
            play = False
        if timer.time() - start > 30:
            mixer.music.stop()
            main_s.stop()
            end_s.play()
            while run:
                for e in event.get():
                    if e.type == QUIT:
                        run = False
                w.blit(back, (0, 0))
                torches.draw(w)
                player.state = 'cheer'
                player.update()
                w.blit(won[0], (255 - 2, 350 - 2))
                w.blit(won[1], (255, 350))
                display.update()
        display.update()
        clock.tick(60)
