from pygame import *
import pygame.time


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, s):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < w - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < h - 80:
            self.rect.y += self.speed
        self.reset()


class Enemy(GameSprite):
    direction = "l"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "r"
        if self.rect.x >= w - 85:
            self.direction = "l"
        if self.direction == "l":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        self.reset()


class Wall(sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.w = w
        self.h = h
        self.s = Surface([self.w, self.h])
        self.s.fill((154, 205, 50))
        self.rect = self.s.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        win.blit(self.s, (self.rect.x, self.rect.y))


def collide():
    if sprite.collide_rect(player, monster):
        return True
    for w in walls:
        if sprite.collide_rect(player, w):
            return True
    return False


w = 700
h = 500
win = display.set_mode((w, h))
display.set_caption("Labirynth")
background = transform.scale(image.load("back.jpg"), (w, h))
clock = time.Clock()
player = Player('monkey.png', 5, h - 80, 4)
monster = Enemy('tiger.png', w - 80, 280, 2)
prize = GameSprite('bananas.png', w - 100, h - 80, 0)
walls = [
    Wall(100, 20, 450, 10),
    Wall(100, 480, 350, 10),
    Wall(100, 20, 10, 380),
    Wall(200, 130, 10, 350),
    Wall(450, 130, 10, 360),
    Wall(300, 20, 10, 350),
    Wall(390, 120, 130, 10)
]
font.init()
font = font.SysFont('Impact', 70)
won = font.render('YOU WON!', True, (255, 215, 0))
lost = font.render('YOU LOST!', True, (180, 0, 0))
mixer.init()
mixer.music.load('jungles.mp3')
mixer.music.play()
yummy = mixer.Sound('drink.mp3')
kick = mixer.Sound('kick.ogg')

f = g = True
while f:
    for e in event.get():
        if e.type == QUIT:
            f = False
    win.blit(background, (0, 0))
    for wall in walls:
        wall.draw()
    prize.reset()
    monster.update()
    player.update()
    if collide():
        win.blit(lost, (200, 200))
        kick.play()
        display.update()
        clock.tick(60)
        g = False
    if sprite.collide_rect(player, prize):
        win.blit(won, (200, 200))
        yummy.play()
        display.update()
        clock.tick(60)
        g = False
    if not g:
        player.rect.x = 5
        player.rect.y = h - 80
        g = True
        pygame.time.wait(300)
    display.update()
    clock.tick(60)