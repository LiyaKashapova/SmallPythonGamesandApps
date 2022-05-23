from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, s, w, h):
        super().__init__()
        self.image = transform.scale(image.load(i), (w, h))
        self.speed = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < wh - 100:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < wh - 100:
            self.rect.y += self.speed

ww = 600
wh = 500
back = transform.scale(image.load('back.png'), (ww, wh))
w = display.set_mode((ww, wh))
display.set_caption('Catch Falafel')
display.set_icon(image.load('saitama.png'))
w.blit(back, (0, 0))

racket1 = Player('platel.png', 30, 200, 4, 50, 150)
racket2 = Player('plater.png', 520, 200, 4, 50, 150)
ball = GameSprite('falafel.png', 200, 200, 4, 50, 50)

font.init()
f = font.SysFont('verdana', 40, bold=True)
losel = [f.render('Fubuki Lost', True, (180, 0, 0)), f.render('the Falafel!', True, (180, 0, 0))]
loser = [f.render('Genos Lost', True, (180, 0, 0)), f.render('the Falafel!', True, (180, 0, 0))]

game = play = True
clock = time.Clock()
sx = sy = 5

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if play:
        w.blit(back, (0, 0))
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += sx
        ball.rect.y += sy
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            sx *= -1
            sy *= 1
        if ball.rect.y > wh - 50 or ball.rect.y < 0:
            sy *= -1
        if ball.rect.x < 0:
            finish = True
            w.blit(losel[0], (180, 280))
            w.blit(losel[1], (180, 330))
            game_over = True
        if ball.rect.x > ww:
            finish = True
            w.blit(loser[0], (180, 280))
            w.blit(loser[1], (180, 330))
            game_over = True
        ball.reset()
        racket1.reset()
        racket2.reset()
    display.update()
    clock.tick(40)

