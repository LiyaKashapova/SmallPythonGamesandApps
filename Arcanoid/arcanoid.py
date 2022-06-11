from pygame import *
import time as timer


class Area:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)


class Picture(Area):
    def __init__(self, i, x, y, w, h):
        Area.__init__(self, x, y, w, h)
        self.image = transform.scale(image.load(i), (w, h))

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


init()
w = display.set_mode((500, 500))
display.set_caption('Mass Effect Arcade')
display.set_icon(image.load('Shepard.png'))
back = transform.scale(image.load('cosmic.png'), (500, 500))
clock = time.Clock()

ball = Picture('crucible.png', 160, 300, 50, 52)
platform = Picture('normandy.png', 200, 400, 100, 40)

ma = 9
ms = []
for j in range(3):
    x = 5 + (27.5 * j)
    y = 5 + (55 * j)
    for i in range(ma):
        p = Picture('reaper.png', x, y, 50, 133)
        ms.append(p)
        x += 55
    ma -= 1

mixer.init()
mt = mixer.Sound('battle.mp3')
mt.set_volume(0.1)
mt.play()
rs = mixer.Sound('reaper.mp3')
rs.set_volume(0.1)
vs = mixer.Sound('victory.mp3')
vs.set_volume(0.5)

game = mr = ml = False
bx = by = 5

while not game:
    for e in event.get():
        if e.type == QUIT:
            game = True
        if e.type == KEYDOWN:
            if e.key == K_d:
                mr = True
            if e.key == K_a:
                ml = True
        if e.type == KEYUP:
            if e.key == K_d:
                mr = False
            if e.key == K_a:
                ml = False
    if mr and platform.rect.x <= (500 - platform.rect.width):
        platform.rect.x += 5
    if ml and platform.rect.x >= 5:
        platform.rect.x -= 5
    ball.rect.x += bx
    ball.rect.y += by
    if ball.rect.y < 0 or ball.rect.colliderect(platform.rect):
        by *= -1
    if ball.rect.x < 0 or ball.rect.x > (500 - ball.rect.width):
        bx *= -1
    w.blit(back, (0, 0))
    for m in ms:
        if m.rect.colliderect(ball.rect):
            ms.remove(m)
            by *= -1
        else:
            m.draw()
    platform.draw()
    ball.draw()
    if ball.rect.y > platform.rect.y + platform.rect.height:
        w.blit(font.SysFont('impact', 60).render('YOU LOSE', True, (255, 0, 0)), (140, 220))
        display.update()
        mt.fadeout(1000)
        rs.play()
        timer.sleep(3)
        game = True
    if len(ms) == 0:
        w.blit(font.SysFont('impact', 60).render('YOU WIN', True, (0, 191, 255)), (150, 220))
        display.update()
        mt.fadeout(500)
        vs.play()
        timer.sleep(5)
        game = True
    display.update()
    clock.tick(40)