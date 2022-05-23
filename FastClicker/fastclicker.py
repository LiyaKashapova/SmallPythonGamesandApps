import pygame
from random import randint


class Area:
    def __init__(self, x, y, w, h, c=(200, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = c

    def color(self, c):
        self.color = c

    def fill(self):
        pygame.draw.rect(w, self.color, self.rect)

    def outline(self):
        pygame.draw.rect(w, (0, 0, 0), self.rect, 5)


class Label(Area):
    def set_text(self, text, color, f):
        self.text = pygame.font.SysFont('verdana', f).render(text, True, color)

    def draw(self, sx, sy):
        self.fill()
        w.blit(self.text, (self.rect.x + sx, self.rect.y + sy))


pygame.init()
pygame.font.init()
w = pygame.display.set_mode((500, 300))
pygame.display.set_caption('Fast Clicker')
pygame.display.set_icon(pygame.image.load('ico.jpg'))
w.fill((200, 255, 255))
clock = pygame.time.Clock()

cards = []
x = 70
for i in range(4):
    card = Label(x, 170, 70, 100, (255, 255, 0))
    card.outline()
    card.set_text('CLICK', (0, 0, 0), 16)
    cards.append(card)
    x += 100

wait = 0
while 1:
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
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            for i in range(len(cards)):
                if cards[i].rect.collidepoint(x, y):
                    if i == click:
                        cards[i].color = (0, 255, 51)
                    else:
                        cards[i].color = (255, 0, 0)
                    cards[i].fill()
                    cards[i].outline()
    pygame.display.update()
    clock.tick(40)
