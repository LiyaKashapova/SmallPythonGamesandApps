from pygame import *
from random import randint
import time as t


class Area:
    def __init__(self, x, y, w, h, c=(200, 255, 255)):
        self.rect = Rect(x, y, w, h)
        self.color = c

    def fill(self, w):
        draw.rect(w, self.color, self.rect)

    def outline(self, w):
        draw.rect(w, (0, 0, 0), self.rect, 5)


class Label(Area):
    def set_text(self, text, color, f):
        self.text = font.SysFont('verdana', f).render(text, True, color)

    def draw(self, w, sx, sy):
        self.fill(w)
        self.outline(w)
        w.blit(self.text, (self.rect.x + sx, self.rect.y + sy))


init()
font.init()
w = display.set_mode((500, 300))
display.set_caption('Fast Clicker')
display.set_icon(transform.scale(image.load('ico.jpg'), (50, 50)))
w.fill((200, 255, 255))
clock = time.Clock()

ttext = Label(50, 10, 0, 0, (200, 255, 255))
ttext.set_text('Time:', (0, 0, 0), 30)
stext = Label(330, 10, 0, 0, (200, 255, 255))
stext.set_text('Score:', (0, 0, 0), 30)
timer = Label(65, 60, 0, 0, (200, 255, 255))
timer.set_text('0', (0, 0, 0), 30)
score = Label(365, 60, 0, 0, (200, 255, 255))
score.set_text('0', (0, 0, 0), 30)

cards = []
x = 70
for i in range(4):
    card = Label(x, 170, 70, 100, (255, 255, 0))
    card.outline(w)
    card.set_text('CLICK', (0, 0, 0), 16)
    cards.append(card)
    x += 100

stime = ctime = t.time()
wait = points = 0
run = True
while run:
    if wait == 0:
        wait = 20
        click = randint(0, len(cards) - 1)
        for i in range(len(cards)):
            cards[i].color = (255, 255, 0)
    else:
        wait -= 1
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            for i in range(len(cards)):
                if cards[i].rect.collidepoint(x, y):
                    if i == click:
                        cards[i].color = (0, 255, 51)
                        points += 1
                    else:
                        cards[i].color = (255, 0, 0)
                        if points > 0:
                            points -= 1
                    cards[i].fill(w)
                    cards[i].outline(w)
                    score.set_text(str(points), (0, 0, 0), 30)
    ntime = t.time()
    if round(ntime) - round(ctime) == 1:
        timer.set_text(str(round(ntime) - round(stime)), (0, 0, 0), 30)
        ctime = ntime
    w.fill((200, 255, 255))
    for i in range(len(cards)):
        if i == click:
            cards[i].draw(w, 10, 30)
        else:
            cards[i].fill(w)
        cards[i].outline(w)
    stext.draw(w, 20, 20)
    ttext.draw(w, 20, 20)
    timer.draw(w, 20, 20)
    score.draw(w, 20, 20)
    if ntime - stime > 10:
        f = Label(0, 0, 500, 300, (255, 0, 0))
        f.set_text('Time\'s up!', (0, 0, 0), 60)
        f.draw(w, 80, 100)
        display.update()
        t.sleep(2)
        run = False
    if points > 0:
        f = Label(0, 0, 500, 300, (0, 255, 51))
        f.set_text('You Won!', (0, 0, 0), 60)
        f.draw(w, 110, 100)
        j = Label(0, 220, 500, 300, (0, 255, 51))
        j.set_text('Time score: ' + str(round(ntime) - round(stime)) + ' sec', (0, 0, 0), 40)
        j.draw(w, 80, 10)
        display.update()
        t.sleep(3)
        run = False
    display.update()
    clock.tick(60)

