from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, i, x, y, s):
        super().__init__()
        self.image = transform.scale(image.load(i), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = s

    def draw(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < ww - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < wh - 80:
            self.rect.y += self.speed
        self.draw()


class Enemy(GameSprite):
    direction = 'l'

    def update(self):
        if self.rect.x <= 470:
            self.direction = 'r'
        elif self.rect.x >= ww - 85:
            self.direction = 'l'
        if self.direction == 'l':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        self.draw()


class Wall(sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.s = Surface([w, h])
        self.s.fill((154, 205, 50))
        self.rect = self.s.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        w.blit(self.s, (self.rect.x, self.rect.y))


def collide():
    if sprite.collide_rect(player, monster):
        return True
    for wall in walls:
        if sprite.collide_rect(player, wall):
            return True
    return False


init()
ww, wh = 700, 500
w = display.set_mode((ww, wh))
display.set_caption('Labyrinth')
display.set_icon(transform.scale(image.load('bananas.png'), (50, 50)))
back = transform.scale(image.load('back.jpg'), (ww, wh))
clock = time.Clock()
player = Player('monkey.png', 5, wh - 80, 4)
monster = Enemy('tiger.png', ww - 80, 280, 2)
prize = GameSprite('bananas.png', ww - 100, wh - 80, 0)
walls = [Wall(100, 20, 450, 10), Wall(100, 480, 350, 10), Wall(100, 20, 10, 380), Wall(200, 130, 10, 350),
         Wall(450, 130, 10, 360), Wall(300, 20, 10, 350), Wall(390, 120, 130, 10)]
font.init()
f = font.SysFont('Impact', 70)
won = f.render('You WON!', True, (255, 215, 0))
lost = f.render('You LOST!', True, (180, 0, 0))
mixer.init()
mixer.music.load('jungles.mp3')
mixer.music.play()
yummy = mixer.Sound('drink.mp3')
kick = mixer.Sound('kick.ogg')

run = play = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    w.blit(back, (0, 0))
    for wall in walls:
        wall.draw()
    prize.draw()
    monster.update()
    player.update()
    if collide():
        w.blit(lost, (200, 200))
        display.update()
        kick.play()
        play = False
    if sprite.collide_rect(player, prize):
        w.blit(won, (200, 200))
        display.update()
        yummy.play()
        play = False
    if not play:
        player.rect.x = 5
        player.rect.y = wh - 80
        play = True
        time.wait(300)
    display.update()
    clock.tick(60)