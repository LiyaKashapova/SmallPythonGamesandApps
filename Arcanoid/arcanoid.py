import time, pygame


class Area:
    def __init__(self, x=0, y=0, width=10, height=10):
        self.rect = pygame.Rect(x, y, width, height)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height)
        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height))

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


pygame.init()
w = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Mass Effect Arcade')
pygame.display.set_icon(pygame.image.load('Shepard.png'))
back = pygame.transform.scale(pygame.image.load('cosmic.png'), (500, 500))
w.blit(back, (0, 0))
clock = pygame.time.Clock()

ball = Picture('crucible.png', 160, 300, 50, 52)
platform = Picture('normandy.png', 200, 400, 100, 40)

ma = 9
ms = []
for j in range(3):
    y = 5 + (55 * j)
    x = 5 + (27.5 * j)
    for i in range(ma):
        p = Picture('reaper.png', x, y, 50, 133)
        ms.append(p)
        x = x + 55
    ma -= 1

bx = by = 5
mr = ml = False

pygame.mixer.init()
mt = pygame.mixer.Sound('battle.mp3')
rs = pygame.mixer.Sound('reaper.mp3')
vs = pygame.mixer.Sound('victory.mp3')
mt.set_volume(0.1)
mt.play()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_d:
                mr = True
            if e.key == pygame.K_a:
                ml = True
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_d:
                mr = False
            if e.key == pygame.K_a:
                ml = False
        if mr:
            platform.rect.x += 5
        if ml:
            platform.rect.x -= 5
    ball.rect.x += bx
    ball.rect.y += by
    if ball.rect.y < 0 or ball.rect.colliderect(platform.rect):
        by *= -1
    if ball.rect.x < 0 or ball.rect.x > 450:
        bx *= -1
    if ball.rect.y > platform.rect.y + platform.rect.height:
        w.blit(pygame.font.SysFont('impact', 60).render('YOU LOSE', True, (255, 0, 0)), (140, 220))
        pygame.display.update()
        mt.fadeout(1000)
        rs.set_volume(0.1)
        rs.play()
        rs.fadeout(5000)
        time.sleep(3)
        quit()
        exit()
    if len(ms) == 0:
        w.blit(pygame.font.SysFont('impact', 60).render('YOU WIN', True, (0, 191, 255)), (150, 220))
        pygame.display.update()
        mt.fadeout(500)
        vs.play()
        time.sleep(5)
        quit()
        exit()
    w.blit(back, (0, 0))
    for m in ms:
        if m.rect.colliderect(ball.rect):
            ms.remove(m)
            by *= -1
        else:
            m.draw()
    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)