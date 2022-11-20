from pygame import *
import time as timer


class Area:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)


class Picture(Area):
    def __init__(self, i, x, y, w, h):
        super().__init__(x, y, w, h)
        self.image = transform.scale(image.load(i), (w, h))

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


init()
w = display.set_mode((500, 500))
display.set_caption('Mass Effect Arcade')
display.set_icon(transform.scale(image.load('Shepard.png'), (50, 50)))
clock = time.Clock()

mixer.init()
mixer.music.load('battle.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
rs = mixer.Sound('reaper.mp3')
rs.set_volume(0.1)
vs = mixer.Sound('victory.mp3')
vs.set_volume(0.5)

back = transform.scale(image.load('cosmic.png'), (500, 500))
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

game, mr, ml = True, False, False
bx, by = 5, -5

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
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
    if mr and platform.rect.x <= 500 - platform.rect.width:
        platform.rect.x += 5
    if ml and platform.rect.x >= 5:
        platform.rect.x -= 5
    ball.rect.x += bx
    ball.rect.y += by
    if ball.rect.y <= 5 or ball.rect.colliderect(platform.rect):
        by *= -1
    if ball.rect.x <= 5 or ball.rect.x >= 500 - platform.rect.width:
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
    if ball.rect.y > platform.rect.y:
        w.blit(font.SysFont('impact', 60).render('You Lost', True, (255, 0, 0)), (140, 220))
        display.update()
        mixer.music.fadeout(1000)
        rs.play()
        timer.sleep(3)
        quit()
    if len(ms) == 0:
        w.blit(font.SysFont('impact', 60).render('You Won', True, (0, 191, 255)), (150, 220))
        display.update()
        mixer.music.fadeout(500)
        vs.play()
        timer.sleep(5)
        quit()
    display.update()
    clock.tick(30)