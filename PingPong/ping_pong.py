from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, s, w, h):
        super().__init__()
        self.image = transform.scale(image.load(i), (w, h))
        self.speed = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < wh - 150:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < wh - 150:
            self.rect.y += self.speed


ww, wh = 600, 500
back = transform.scale(image.load('back.png'), (ww, wh))
w = display.set_mode((ww, wh))
display.set_caption('Catch Falafel')
display.set_icon(image.load('saitama.png'))

racketl = Player('platel.png', 30, 200, 5, 50, 150)
racketr = Player('plater.png', 520, 200, 5, 50, 150)
ball = GameSprite('falafel.png', 200, 200, 5, 50, 50)

font.init()
f = font.SysFont('verdana', 40, bold=True)
losel = [f.render('Fubuki Lost', True, (180, 0, 0)), f.render('the Falafel!', True, (180, 0, 0))]
loser = [f.render('Genos Lost', True, (180, 0, 0)), f.render('the Falafel!', True, (180, 0, 0))]

mixer.init()
mixer.music.load('main.mp3')
mixer.music.set_volume(0.3)
hit = mixer.Sound('hit.mp3')
hit.set_volume(0.3)

game = play = True
clock = time.Clock()
mixer.music.play(-1)
sx = sy = 5

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if play:
        w.blit(back, (0, 0))
        racketl.update_l()
        racketr.update_r()
        ball.rect.x += sx
        ball.rect.y += sy
        if sprite.collide_rect(racketl, ball) or sprite.collide_rect(racketr, ball):
            sx *= -1
            hit.play()
        if ball.rect.y < 0 or ball.rect.y > wh - ball.rect.height:
            sy *= -1
            hit.play()
        if ball.rect.x < 0:
            play = False
            w.blit(losel[0], (180, 280))
            w.blit(losel[1], (180, 330))
        if ball.rect.x > ww - ball.rect.width:
            play = False
            w.blit(loser[0], (180, 280))
            w.blit(loser[1], (180, 330))
        ball.draw()
        racketl.draw()
        racketr.draw()
    display.update()
    clock.tick(40)