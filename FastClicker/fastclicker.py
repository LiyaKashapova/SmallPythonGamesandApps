from pygame import *
from random import randint
import time as t
import sys


class Area:
    def __init__(self, x, y, w, h, c=(200, 255, 255)):
        self.rect = Rect(x, y, w, h)
        self.color = c

    def color(self, c):
        self.color = c

    def fill(self):
        draw.rect(w, self.color, self.rect)

    def outline(self):
        draw.rect(w, (0, 0, 0), self.rect, 5)


class Label(Area):
    def set_text(self, text, color, f):
        self.text = font.SysFont('verdana', f).render(text, True, color)

    def draw(self, sx, sy):
        self.fill()
        w.blit(self.text, (self.rect.x + sx, self.rect.y + sy))


init()
font.init()
w = display.set_mode((500, 300))
display.set_caption('Fast Clicker')
display.set_icon(transform.scale(image.load('ico.jpg'), (50, 50)))
w.fill((200, 255, 255))
clock = time.Clock()

ttext = Label(0, 0, 50, 50, (200, 255, 255))
ttext.set_text('Time: ', (0, 0, 0), 30)
ttext.draw(20, 20)
stext = Label(370, 0, 50, 50, (200, 255, 255))
stext.set_text('Score: ', (0, 0, 0), 30)
stext.draw(20, 20)
timer = Label(50, 55, 50, 40, (200, 255, 255))
timer.set_text('0', (0, 0, 0), 30)
timer.draw(0, 0)
score = Label(430, 55, 50, 40, (200, 255, 255))
score.set_text('0', (0, 0, 0), 30)
score.draw(0, 0)

cards = []
x = 70
for i in range(4):
    card = Label(x, 170, 70, 100, (255, 255, 0))
    card.outline()
    card.set_text('CLICK', (0, 0, 0), 16)
    cards.append(card)
    x += 100

stime = ctime = t.time()
wait = points = 0
game = 1
while game:
    if wait == 0:
        wait = 20
        click = randint(0, len(cards) - 1)  # від 0 до 3 (кількість карточок - 1)
        for i in range(len(cards)):
            cards[i].color = (255, 255, 0)
            if i == click:
                cards[i].draw(10, 30)
            else:
                cards[i].fill()
            cards[i].outline()
    else:
        wait -= 1
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            for i in range(len(cards)):
                if cards[i].rect.collidepoint(x, y):
                    if i == click:
                        cards[i].color = (0, 255, 51)
                        points += 1
                    else:
                        cards[i].color = (255, 0, 0)
                        points -= 1
                    cards[i].fill()
                    cards[i].outline()
                    score.set_text(str(points), (0, 0, 100), 40)
                    score.draw(0, 0)
    ntime = t.time()
    if round(ntime) - round(ctime) == 1:
        timer.set_text(str(round(ntime) - round(stime)), (0, 0, 0), 40)
        timer.draw(0, 0)
        ctime = ntime
    if ntime - stime > 10:
        b = Label(0, 0, 500, 300, (250, 128, 114))
        b.set_text('Time\'s up!', (0, 0, 0), 60)
        b.draw(80, 100)
        display.update()
        t.sleep(2)
        game = 0
    if points > 0:
        b = Label(0, 0, 500, 300, (0, 100, 0))
        b.set_text('You Won!', (0, 0, 0), 40)
        b.draw(110, 100)
        rtime = Label(90, 230, 250, 250, (0, 100, 0))
        rtime.set_text('Time score: ' + str(round(ntime) - round(stime)) + ' sec', (0, 0, 0), 40)
        rtime.draw(0, 0)
        display.update()
        t.sleep(3)
        game = 0
    display.update()
    clock.tick(40)