from pygame import *
import time as timer


class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames_r = [transform.scale(image.load('Player/run1.png'), (200, 200)),
                         transform.scale(image.load('Player/run2.png'), (200, 200)),
                         transform.scale(image.load('Player/run3.png'), (200, 200))]
        self.frames_l = [transform.flip(self.frames_r[0], True, False), transform.flip(self.frames_r[1], True, False),
                         transform.flip(self.frames_r[2], True, False)]
        self.jump_i = transform.scale(image.load('Player/jump.png'), (200, 200))
        self.fall = transform.scale(image.load('Player/fall.png'), (200, 200))
        self.stand = transform.scale(image.load('Player/stand.png'), (200, 200))
        self.cheer = transform.scale(image.load('Player/cheer.png'), (200, 200))
        self.image = self.stand
        self.rect = self.image.get_rect()
        self.direction = "r"
        self.rect.x = self.image.get_width()
        self.rect.y = self.image.get_height()
        self.sx = 0
        self.sy = 0
        self.level = None

    def calc_grav(self):
        if self.sy == 0:
            self.sy = 1
        else:
            self.sy += .35
        if self.rect.y >= wh - self.rect.height and self.sy >= 0:
            self.sy = 0
            self.rect.y = wh - self.rect.height
        self.rect.y += 1
        platforms = sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 1
        if len(platforms) > 0 or self.sy == 0:
            self.image = self.stand
        else:
            self.image = self.fall

    def jump(self):
        self.rect.y += 1
        platforms = sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 1
        if len(platforms) > 0 or self.rect.bottom >= wh:
            self.sy = -10
        self.image = self.jump_i

    def update(self):
        self.calc_grav()
        self.rect.x += self.sx
        pos = self.rect.x + self.level.world_shift
        frame = (pos // 30) % len(self.frames_r)
        if self.direction == "r" and self.sx != 0:
            self.image = self.frames_r[frame]
        elif self.direction == "l" and self.sx != 0:
            self.image = self.frames_l[frame]
        blocks = sprite.spritecollide(self, self.level.platforms, False)
        for block in blocks:
            if self.sx > 0:
                self.rect.right = block.rect.left
            elif self.sx < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.sy
        blocks = sprite.spritecollide(self, self.level.platforms, False)
        for block in blocks:
            if self.sy > 0:
                self.rect.bottom = block.rect.top
            elif self.sy < 0:
                self.rect.top = block.rect.bottom
            self.sy = 0
            if isinstance(block, MovingPlatform):
                self.rect.x += block.sx

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Platform(sprite.Sprite):
    def __init__(self, i, iw, ih):
        super().__init__()
        self.image = transform.scale(image.load(i), (iw, ih))
        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    sx = sy = bt = bb = bl = br = 0
    player = level = None

    def update(self):
        self.rect.x += self.sx
        if sprite.collide_rect(self, self.player):
            if self.sx < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right
        self.rect.y += self.sy
        if sprite.collide_rect(self, self.player):
            if self.sy < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
        if self.rect.bottom > self.bb or self.rect.top < self.bt:
            self.sy *= -1
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.bl or cur_pos > self.br:
            self.sx *= -1


class Level(object):
    def __init__(self, p, bi, iw, ih):
        self.platforms = sprite.Group()
        self.enemies = sprite.Group()
        self.player = p
        self.background = transform.scale(image.load(bi), (iw, ih))
        self.world_shift = 0
        self.level_limit = -ww * 2 - 50

    def update(self):
        self.platforms.update()
        self.enemies.update()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.platforms.draw(screen)
        self.enemies.draw(screen)

    def shift_world(self, sx):
        self.world_shift += sx
        for platform in self.platforms:
            platform.rect.x += sx
        for enemy in self.enemies:
            enemy.rect.x += sx


class Level_1(Level):
    def __init__(self, p):
        Level.__init__(self, p, 'level1.jpg', 2400, 700)
        level = [[210, 70, 500, 550],  # platform width, height, x, and y
                 [210, 70, 800, 450],
                 [210, 70, 1000, 550],
                 [210, 70, 1120, 330],
                 [210, 70, 1700, 280]]
        for platform in level:
            block = Platform('rocks.jpg', platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platforms.add(block)
        block = MovingPlatform('rocks.jpg', 200, 70)
        block.rect.x = 1350
        block.rect.y = 280
        block.bl = 1350
        block.br = 1500
        block.sx = 1
        block.player = self.player
        block.level = self
        self.platforms.add(block)


class Level_2(Level):
    def __init__(self, p):
        Level.__init__(self, p, 'level2.jpg', 2400, 700)
        level = [[210, 70, 500, 600],  # platform width, height, x, and y
                 [210, 70, 800, 500],
                 [210, 70, 1100, 600],
                 [210, 70, 1220, 380]]
        for platform in level:
            block = Platform('rocks.jpg', platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platforms.add(block)
        block = MovingPlatform('rocks.jpg', 70, 70)
        block.rect.x = 1400
        block.rect.y = 200
        block.bt = 100
        block.bb = 450
        block.sy = -1
        block.player = self.player
        block.level = self
        self.platforms.add(block)


init()
ww = 1200
wh = 700
w = display.set_mode((ww, wh))
display.set_caption("Small Platformer")
display.set_icon(image.load('icon.png'))
f = font.SysFont('Impact', 60)

level_num = 0
player = Player()
levels = [Level_1(player), Level_2(player)]
cur_level = levels[level_num]
player.level = cur_level

run = True
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            quit()
            exit()
        if e.type == KEYDOWN:
            if e.key == K_a:
                player.sx = -5
                player.direction = 'l'
            if e.key == K_d:
                player.sx = 5
                player.direction = 'r'
            if e.key == K_SPACE:
                player.jump()
        if e.type == KEYUP:
            if e.key == K_a and player.sx < 0:
                player.sx = 0
            if e.key == K_d and player.sx > 0:
                player.sx = 0
    player.update()
    cur_level.update()
    if player.rect.x >= ww - 200:
        diff = player.rect.x - (ww - 200)
        player.rect.x = ww - 200
        cur_level.shift_world(-diff)
    if player.rect.x <= 200:
        diff = 200 - player.rect.x
        player.rect.x = 200
        cur_level.shift_world(diff)
    current_position = player.rect.x + cur_level.world_shift
    if current_position < cur_level.level_limit:
        player.rect.x = 120
        if level_num < len(levels) - 1:
            level_num += 1
            w.blit(f.render('You managed to get to the icy island!', True, (180, 0, 0)), (150, 300))
            display.update()
            timer.sleep(2)
            cur_level = levels[level_num]
            player.level = cur_level
        else:
            w.blit(f.render('You Won!', True, (180, 0, 0)), (ww / 2 - 100, wh / 2))
            display.update()
            timer.sleep(3)
            run = False
    cur_level.draw(w)
    player.draw(w)
    clock.tick(60)
    display.update()
