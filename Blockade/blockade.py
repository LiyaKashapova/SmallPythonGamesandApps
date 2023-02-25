from pygame import *
import time as timer
from random import choice

images = {
    'back': transform.scale(image.load('images/background.png'), (1280, 720)),
    'player': {'run': [transform.scale(image.load("images/player/run1.png"), (50, 50)),
                       transform.scale(image.load("images/player/run2.png"), (50, 50))],
               'climb': [transform.scale(image.load("images/player/climb1.png"), (50, 50)),
                         transform.scale(image.load("images/player/climb2.png"), (50, 50))],
               'shoot': transform.scale(image.load("images/player/shoot.png"), (50, 50))},
    'enemy': [transform.scale(image.load(f"images/robot/robot{i}.png"), (50, 50)) for i in range(1, 9)],
    'boss': [transform.scale(image.load(f"images/boss/walk{i}.png"), (80, 80)) for i in range(1, 9)] +
            [transform.scale(image.load(f"images/boss/attack{i}.png"), (80, 80)) for i in range(1, 4)],
    'spheres': [transform.scale(image.load(f"images/boss/sphere{i}.png"), (40, 40)) for i in range(1, 9)],
    'crystal': transform.scale(image.load("images/crystal.png"), (50, 50)),
    'obs': [transform.scale(image.load("images/obs.png"), (40, 120)),
            transform.scale(image.load("images/obs.png"), (20, 60)),
            transform.scale(image.load("images/obs.png"), (10, 30)),
            transform.scale(image.load("images/obs.png"), (5, 15))],
    'key': transform.scale(image.load("images/key.png"), (40, 50)),
    'chest_opened': transform.scale(image.load("images/chest/chest4.png"), (80, 60)),
    'chest_closed': transform.scale(image.load("images/chest/chest1.png"), (80, 60)),
    'stair': transform.scale(image.load("images/stair.png"), (50, 180)),
    'portal': transform.scale(image.load("images/portal.png"), (100, 100)),
    'platform': transform.scale(image.load("images/platform.jpg"), (40, 40)),
    'strike': transform.scale(image.load("images/lasers.png"), (25, 25)),
    'nothing': transform.scale(image.load("images/nothing.png"), (40, 40))
}

ww, wh = 1280, 700
w = display.set_mode((ww, wh))
display.set_caption("Blockade")
display.set_icon(transform.scale(image.load('images/icon.png'), (50, 50)))

mixer.init()
music = mixer.Channel(1)
strike_sound, kick_sound, fire_sound, run_sound, key_sound, crystal_sound, obs_sound, teleport_sound, click_sound,\
    chest_sound, game_sound, menu_sound, end_sound, bonus_sound = mixer.Sound('sounds/strike.mp3'),\
    mixer.Sound('sounds/lasers.mp3'),  mixer.Sound('sounds/fire.mp3'), mixer.Sound('sounds/running.mp3'),\
    mixer.Sound('sounds/backpack.mp3'), mixer.Sound('sounds/crystal.mp3'), mixer.Sound('sounds/remove.mp3'),\
    mixer.Sound('sounds/teleport.wav'), mixer.Sound('sounds/click.wav'), mixer.Sound('sounds/metal.mp3'),\
    mixer.Sound('sounds/game.mp3'), mixer.Sound('sounds/menu.mp3'), mixer.Sound('sounds/game_over.wav'), \
    mixer.Sound('sounds/bonus.mp3')
crystal_sound.set_volume(0.3)


class GameSprite(sprite.Sprite):
    def __init__(self, x, y, i, speed=0, side='right'):
        super().__init__()
        self.image = i
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed
        self.side = side

    def update(self, camera):
        w.blit(self.image, camera.apply(self))


class Player(GameSprite):
    ammunition = cur_frame = rate = 0
    strikes = sprite.Group()
    state = 'move'  # move, climb
    running = mixer.Channel(2)

    def move(self):
        keys = key.get_pressed()
        if keys[K_a] or keys[K_d]:
            if not self.running.get_busy():
                self.running.play(run_sound, -1)
            if self.rate == 5:
                self.cur_frame += 1
                self.rate = 0
            if self.cur_frame == 2:
                self.cur_frame = 0
            self.rate += 1
        if keys[K_a]:
            self.rect.x -= self.speed
            self.image = transform.flip(images['player']['run'][self.cur_frame], True, False)
            self.side = 'left'
        if keys[K_d]:
            self.rect.x += self.speed
            self.image = images['player']['run'][self.cur_frame]
            self.side = 'right'

    def climb(self, stair):
        keys = key.get_pressed()
        if keys[K_w] or keys[K_s]:
            if self.running.get_busy():
                self.running.stop()
            if self.rate == 5:
                self.cur_frame += 1
                self.rate = 0
            if self.cur_frame == 2:
                self.cur_frame = 0
            self.rate += 1
            self.image = images['player']['climb'][self.cur_frame]
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if self.rect.y <= (stair.rect.y - 40):
            self.rect.y = stair.rect.y - 40
        if self.rect.y >= (stair.rect.y + 130):
            self.rect.y = stair.rect.y + 130

    def update(self, camera):
        keys = key.get_pressed()
        if self.state == 'move':
            if not keys[K_d] and not keys[K_a]:
                if self.running.get_busy():
                    self.running.stop()
                if self.side == 'right':
                    self.image = images['player']['shoot']
                else:
                    self.image = transform.flip(images['player']['shoot'], True, False)
            if keys[K_SPACE] and self.ammunition:
                self.ammunition -= 1
                self.strikes.add(MovingSprite(self.rect.centerx, self.rect.centery - 10, images['strike'], 3, self.side))
                strike_sound.play()
        self.strikes.update(camera)
        w.blit(self.image, camera.apply(self))


class MovingSprite(GameSprite):

    def update(self, camera):
        if self.side == 'right':
            self.rect.x += self.speed
        if self.side == 'left':
            self.rect.x -= self.speed
        w.blit(self.image, camera.apply(self))


class Enemy(MovingSprite):
    rate = cur_frame = 0

    def update(self, camera):
        if self.rate == 3:  # walking animation
            self.cur_frame += 1
            self.rate = 0
        if self.cur_frame == 8:
            self.cur_frame = 0
        self.rate += 1
        if self.side == 'right':
            self.rect.x += self.speed
            self.image = images['enemy'][self.cur_frame]
        if self.side == 'left':
            self.rect.x -= self.speed
            self.image = transform.flip(images['enemy'][self.cur_frame], True, False)
        w.blit(self.image, camera.apply(self))


class Sphere(GameSprite):

    def update(self, camera):
        self.rect.y += self.speed
        w.blit(self.image, camera.apply(self))


class Boss(MovingSprite):
    rate = cur_frame = 0
    spheres = sprite.Group()

    def update(self, camera):
        if self.rate == 3:  # walking animation
            self.cur_frame += 1
            self.rate = 0
        if self.cur_frame == 8 and self.rate == 1:  # hitting starts
            fire_sound.play()
            self.spheres.add(Sphere(self.rect.centerx, self.rect.centery, choice(images['spheres']), 5))
        if self.cur_frame == 11:
            self.cur_frame = 0
        self.rate += 1
        if self.side == 'right':
            self.rect.x += self.speed
            self.image = images['boss'][self.cur_frame]
        if self.side == 'left':
            self.rect.x -= self.speed
            self.image = transform.flip(images['boss'][self.cur_frame], True, False)
        w.blit(self.image, camera.apply(self))
        self.spheres.update(camera)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_config(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, cw, ch = camera
    l, t = -l + ww / 2, -t + wh / 2
    l = min(0, l)
    l = max(-(camera.width - ww), l)
    t = max(-(camera.height - wh), t)
    t = min(0, t)
    return Rect(l, t, cw, ch)


font.init()
f, f2, f3 = font.Font('fonts/LifeForm.ttf', 200), \
            font.Font('fonts/Surfing Capital.ttf', 60), font.Font('fonts/mrsmonstercond.ttf', 45)
white = (255, 255, 255)


class Level:
    level = []
    level_width, level_height, shrink, shrink_frame, chest_key, obs_key = 0, 0, 0, 0, False, False
    platforms, block_r, block_l, enemies = sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()
    stairs, crystals, chest_keys, chests = sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()
    obs, portal = sprite.Group(), sprite.Sprite()

    mes = {'e_chest': f2.render('Press E to pick the chest key!', True, white),
           'e_look': f2.render('Press E to look for the antigraviton!', True, white),
           'e_open': f2.render('Press E to remove the gravitational trap!', True, white),
           'key_chest': f2.render('You need a key to open the chest!', True, white),
           'key_obs': f2.render('You need a key to remove the trap!', True, white),
           'space': f2.render('Press SPACE to shoot lasers', True, white),
           'no_ammo': f2.render('First collect CRYSTALS to shoot!', True, white)
           }

    def __init__(self, player):  # creating main objects based on symbols in 'level' array
        self.camera = Camera(camera_config, self.level_width, self.level_height)
        self.player = player
        x = y = 0
        for row in self.level:
            for sym in row:
                if sym == 'r':
                    self.block_r.add(GameSprite(x, y, images['nothing']))
                elif sym == 'l':
                    self.block_l.add(GameSprite(x, y, images['nothing']))
                elif sym == '|':
                    self.stairs.add(GameSprite(x, y - 40, images['stair']))
                elif sym == '°':
                    self.crystals.add(GameSprite(x, y, images['crystal']))
                elif sym == '-':
                    self.platforms.add(GameSprite(x, y, images['platform']))
                x += 40
            y += 40
            x = 0

    def clear(self):
        self.platforms.empty()
        self.block_r.empty()
        self.block_l.empty()
        self.enemies.empty()
        self.stairs.empty()
        self.crystals.empty()
        self.chest_keys.empty()
        self.chests.empty()
        self.obs.empty()

    def update(self):
        self.camera.update(self.player)  # shifting player
        flag = True
        for p in self.platforms:  # drawing platforms
            p.update(self.camera)
        for br in self.block_r:  # drawing right blocks
            if sprite.collide_rect(self.player, br):  # prevent player from falling from right side
                self.player.rect.x = br.rect.x - self.player.image.get_width()
            else:
                br.update(self.camera)
        for bl in self.block_l:  # drawing left blocks
            if sprite.collide_rect(self.player, bl):  # prevent player from falling from left side
                self.player.rect.x = bl.rect.x + self.player.image.get_width()
            else:
                bl.update(self.camera)
        for en in self.enemies:  # drawing enemies
            if sprite.spritecollide(en, self.player.strikes, True):  # destroying enemies that ware struck
                kick_sound.play()
                en.kill()
            if sprite.collide_rect(self.player, en):  # checking if any enemy killed the player
                flag = False  # indication that the player lost
            if sprite.spritecollide(en, self.block_r, False):  # flip to left if they reached the right side
                en.side = 'left'
            elif sprite.spritecollide(en, self.block_l, False):  # flip to right if they reached the left side
                en.side = 'right'
            if en:
                en.update(self.camera)
        for s in self.player.strikes:  # drawing spheres
            # destroying spheres that touched blocks
            if sprite.spritecollide(s, self.block_r, False) or sprite.spritecollide(s, self.block_l, False):
                s.kill()
            else:
                s.update(self.camera)
        for s in self.stairs:  # drawing stairs
            if sprite.collide_rect(self.player, s):  # climbing the ladders
                self.player.state = 'climb'
                self.player.climb(s)
            s.update(self.camera)
        for c in self.crystals:  # drawing crystals
            if sprite.collide_rect(self.player, c):  # collecting crystals
                crystal_sound.play()
                self.player.ammunition += 1
                c.kill()
            if c:
                c.update(self.camera)
        keys = key.get_pressed()
        for k in self.chest_keys:  # drawing chest keys
            if sprite.collide_rect(self.player, k):
                w.blit(self.mes['e_chest'], ((ww - self.mes['e_chest'].get_width()) / 2, 50))
                if keys[K_e]:
                    key_sound.play()
                    k.kill()
                    self.chest_key = True
            if k:
                k.update(self.camera)
        for c in self.chests:  # drawing chests
            if sprite.collide_rect(self.player, c) and not self.obs_key:
                if not self.chest_key:
                    w.blit(self.mes['key_chest'], ((ww - self.mes['key_chest'].get_width()) / 2, 50))
                else:
                    w.blit(self.mes['e_look'], ((ww - self.mes['e_look'].get_width()) / 2, 50))
                    if keys[K_e]:
                        chest_sound.play()
                        c.image = images['chest_opened']
                        self.obs_key, self.chest_key = True, False
            c.update(self.camera)
        for o in self.obs:  # drawing obs
            if sprite.collide_rect(self.player, o):
                if self.player.side == 'right':
                    self.player.rect.x = o.rect.x - 50
                else:
                    self.player.rect.x = o.rect.right
                if not self.obs_key:
                    w.blit(self.mes['key_obs'], ((ww - self.mes['key_obs'].get_width()) / 2, 50))
                else:
                    w.blit(self.mes['e_open'], ((ww - self.mes['e_open'].get_width()) / 2, 50))
                    if keys[K_e]:
                        obs_sound.play()
                        self.shrink_frame += 1
                        self.obs_key = False
            if self.shrink_frame > 0:  # shrinking animation
                if self.shrink == 3:
                    self.shrink_frame += 1
                    self.shrink = 0
                if self.shrink_frame == 3:
                    o.kill()
                self.shrink += 1
                o.image = images['obs'][self.shrink_frame]
            if o:
                o.update(self.camera)
        self.portal.update(self.camera)
        if sprite.spritecollide(self.player, self.platforms, False) \
                and not sprite.spritecollide(self.player, self.block_r, False) \
                and not sprite.spritecollide(self.player, self.block_l, False):
            self.player.state = 'move'
            self.player.move()
        if not self.player.ammunition and keys[K_SPACE]:
            w.blit(self.mes['no_ammo'], ((ww - self.mes['no_ammo'].get_width()) / 2, 50))
        self.player.update(self.camera)
        return flag


class Level1(Level):
    level = [
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l l            r               l            l         °     r        r",
        "l  ------------                  -------      ---------------        r",
        "l l | r                             l | r    l | r       l | r       r",
        "l l   r                             l   r    l   r       l   r       r",
        "l l   ° nr                          l     °      r    l      r       r",
        "l  ------                            ------------      -------       r",
        "l     l | r                                          l | r           r",
        "l     l   r                                          l   r           r",
        "l     l       °     r                         l    °     r           r",
        "l      -------------                           ---------             r",
        "l               l | r                         l | r                  r",
        "l               l   r                         l   r                  r",
        "l                                                                    r",
        "----------------------------------------------------------------------"]
    level_width = len(level[0]) * 40
    level_height = len(level) * 40

    def __init__(self):
        player = Player(300, 650, images['player']['shoot'], 10)
        super().__init__(player)
        self.enemies.add(Enemy(400, 480, images['enemy'][0], 3),
                         Enemy(230, 320, images['enemy'][0], 3),
                         Enemy(1800, 160, images['enemy'][0], 3),
                         Enemy(1700, 320, images['enemy'][0], 3))
        self.obs.add(GameSprite(1000, 580, images['obs'][0]), GameSprite(2600, 580, images['obs'][0]))
        self.chest_keys.add(GameSprite(210, 340, images['key']), GameSprite(1600, 340, images['key']))
        self.chests.add(GameSprite(450, 150, images['chest_closed']), GameSprite(1400, 150, images['chest_closed']))
        self.portal = GameSprite(2700, 600, images['portal'])


class Level2(Level):
    level = [
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l--------------------------------------------------------------------r",
        "l                                                          l | r     r",
        "l                                                          l   r     r",
        "l  l     °                     °            r       l            °  rr",
        "l   ----------------------------------------         --------------- r",
        "l  l | r                              l | r           l | r          r",
        "l  l   r                              l   r           l   r          r",
        "l l              r              l            °               r       r",
        "l  --------------                -----------------------------       r",
        "l                                l | r                               r",
        "l                                l   r                               r",
        "l    l       °                              °                r       r",
        "l     -------------------------------------------------------        r",
        "l                   l | r                                l | r       r",
        "l                   l   r                                l   r       r",
        "l          °                                         °               r",
        "----------------------------------------------------------------------"]
    level_width = len(level[0]) * 40
    level_height = len(level) * 40

    def __init__(self):
        super().__init__(Player(300, 810, images['player']['shoot'], 10))
        self.enemies.add(Enemy(400, 640, images['enemy'][0], 3),
                         Enemy(230, 320, images['enemy'][0], 3),
                         Enemy(1800, 160, images['enemy'][0], 3),
                         Enemy(1700, 320, images['enemy'][0], 3),
                         Enemy(1700, 480, transform.flip(images['enemy'][0], True, False), 3, 'left'),
                         Enemy(1700, 640, transform.flip(images['enemy'][0], True, False), 3, 'left'),
                         Enemy(230, 480, images['enemy'][0], 3))
        self.obs.add(GameSprite(1700, 410, images['obs'][0]), GameSprite(1000, 100, images['obs'][0]))
        self.chest_keys.add(GameSprite(2350, 500, images['key']), GameSprite(600, 500, images['key']))
        self.chests.add(GameSprite(250, 640, images['chest_closed']))
        self.portal = GameSprite(100, 100, images['portal'])


class Bonus(Level):
    level = [
        "l                                      r",
        "l                                      r",
        "l                                      r",
        "l--------------------------------------r",
        "ll|r                                   r",
        "l                                      r",
        "l                  °                   r",
        "l--------------------------------------r",
        "l                                   l|rr",
        "l                                      r",
        "l                                      r",
        "l--------------------------------------r",
        "ll|r                                   r",
        "l                                      r",
        "l                                      r",
        "l--------------------------------------r"]
    level_width = len(level[0]) * 40
    level_height = len(level) * 40

    def __init__(self):
        super().__init__(Player(400, 560, images['player']['shoot'], 10))
        self.boss = Boss(100, 50, images['boss'][0], 5, 'right')
        self.enemies.add(self.boss)  # consists of Boss & spheres to check collision


class Button:
    def __init__(self, xy, t, bw=470, bh=70, c=(106, 90, 205), t_color=(255, 255, 255)):
        self.image = Surface([bw, bh])
        self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = xy[0], xy[1]
        self.text = f2.render(t, True, t_color)

    def draw(self, shift_x=None, shift_y=5):
        if not shift_x:
            shift_x = (self.rect.width - self.text.get_width()) / 2
        w.blit(self.image, (self.rect.x, self.rect.y))
        w.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))


run, cur_level, level = True, 1, None
clock = time.Clock()

magenta, red, purple = (150, 0, 150), (178, 34, 34), (106, 90, 205)
xy = [(ww / 2, 300), (ww / 2, 450), (ww / 2, 600)]  # menu buttons' coordinates


def level_play(restart=True):
    global run, cur_level, level
    if cur_level == 3:
        return 'bonus'
    if restart:
        if level:
            level.clear()
        if cur_level == 1:
            level = Level1()
        elif cur_level == 2:
            level = Level2()
        if music.get_sound() != game_sound:
            music.play(game_sound, -1)
    btn_pause = Button((1200, 15), 'I I', 50, 50, magenta)
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if btn_pause.rect.collidepoint(x, y):
                    click_sound.play()
                    if level.player.running.get_busy():
                        level.player.running.stop()
                    return 'pause'
        w.blit(images['back'], (0, 0))
        if not level.update():
            if level.player.running.get_busy():
                level.player.running.stop()
            return 'loose'
        w.blit(images['crystal'], (10, 10))
        w.blit(f3.render(f': {level.player.ammunition}', True, white), (60, 10))
        btn_pause.draw(0, -10)
        if sprite.collide_rect(level.player, level.portal):
            if level.player.running.get_busy():
                level.player.running.stop()
            return 'win'
        display.update()
        clock.tick(30)


def pause():
    global run
    elements = [f.render("PAUSE", True, white, red), Button(xy[0], 'CONTINUE'), Button(xy[1], 'RESTART'),
                Button(xy[2], 'BACK TO MENU')]
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if elements[1].rect.collidepoint(x, y):
                    click_sound.play()
                    return None
                elif elements[2].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'level'
                elif elements[3].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'menu'
        w.blit(images['back'], (0, 0))
        w.blit(elements[0], ((ww - elements[0].get_width()) / 2, 70))
        for i in range(1, 4):
            elements[i].draw()
        display.update()
        clock.tick(30)


def menu():
    global run
    elements = [f.render("BLOCKADE", True, white, red), Button(xy[0], 'START GAME'), Button(xy[1], 'HOW TO PLAY'),
                Button(xy[2], 'EXIT GAME')]
    if music.get_sound() != menu_sound:
        music.play(menu_sound, -1)
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if elements[1].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'level'
                elif elements[2].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'rules'
                elif elements[3].rect.collidepoint(x, y):
                    click_sound.play()
                    run = False
        w.blit(images['back'], (0, 0))
        w.blit(elements[0], ((ww - elements[0].get_width()) / 2, 70))
        for i in range(1, 4):
            elements[i].draw()
        display.update()
        clock.tick(30)


def rules():
    global run
    elements = [f.render("BLOCKADE", True, white, red),
                f3.render('Move with WASD. You can only go up and down the stairs.', True, magenta),
                f3.render('Move with WASD. You can only go up and down the stairs.', True, purple),
                f3.render('Use SPACE to shoot. Use E to interact with the world.', True, magenta),
                f3.render('Use SPACE to shoot. Use E to interact with the world.', True, purple),
                Button(xy[2], 'BACK TO MENU')]
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if elements[5].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'menu'
        w.blit(images['back'], (0, 0))
        w.blit(elements[0], ((ww - elements[0].get_width()) / 2, 70))
        draw.rect(w, white, Rect((ww - elements[1].get_width()) / 2 - 50, xy[0][1] - 10, elements[1].get_width() + 100,
                                 (elements[1].get_height() + elements[3].get_height()) + 130))
        w.blit(elements[1], ((ww - elements[1].get_width()) / 2, xy[0][1]))
        w.blit(elements[2], ((ww - elements[1].get_width()) / 2 - 3, xy[0][1]))
        w.blit(elements[3], ((ww - elements[3].get_width()) / 2, xy[1][1]))
        w.blit(elements[4], ((ww - elements[3].get_width()) / 2 - 3, xy[1][1]))
        elements[5].draw()
        display.update()
        clock.tick(30)


def level_complete(result):
    global run, cur_level, level
    game_state = 0  # 0 - level was completed, 1 - won, 2 - lost
    if result == 'win' and cur_level == 3:
        game_state = 1
    elif result == 'loose':
        game_state = 2
        music.play(end_sound)
    teleport_sound.play()
    level.clear()
    headers = [f.render(f'LEVEL {cur_level} DONE', True, purple, red), f.render('YOU WON', True, purple, red),
               f.render('YOU LOST', True, purple, red)]
    elements = []
    if game_state:
        elements = [Button(xy[0], 'RESTART'), Button(xy[1], 'HOW TO PLAY'), Button(xy[2], 'BACK TO MENU')]
    else:
        elements = [Button(xy[0], 'RESTART'), Button(xy[1], 'NEXT LEVEL'), Button(xy[2], 'BACK TO MENU')]
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                if elements[0].rect.collidepoint(x, y):
                    click_sound.play()
                    if game_state == 1:
                        cur_level = 1
                    return 'level'
                elif elements[1].rect.collidepoint(x, y):
                    click_sound.play()
                    if not game_state:
                        cur_level += 1
                        return 'level'
                    return 'rules'
                elif elements[2].rect.collidepoint(x, y):
                    click_sound.play()
                    return 'menu'
        w.blit(images['back'], (0, 0))
        w.blit(headers[game_state], ((ww - headers[game_state].get_width()) / 2, 70))  # header
        for i in range(0, 3):  # buttons
            elements[i].draw()
        display.update()
        clock.tick(30)


def bonus_level():
    global run, level
    if music.get_sound() != bonus_sound:
        music.play(bonus_sound, -1)
    header = f.render('BONUS LEVEL', True, purple, red)
    w.blit(images['back'], (0, 0))
    w.blit(header, ((ww - header.get_width()) / 2, (wh - header.get_height()) / 2))  # header
    display.update()
    timer.sleep(2)
    if level:
        level.boss.spheres.empty()
        level.enemies.empty()
    level = Bonus()
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
        level.enemies.add(level.boss.spheres)
        w.blit(images['back'], (0, 0))
        if not level.update():
            if level.player.running.get_busy():
                level.player.running.stop()
            return 'loose'
        w.blit(images['crystal'], (10, 10))
        w.blit(f3.render(f': {level.player.ammunition}', True, white), (60, 10))
        if not level.enemies.has(level.boss):
            if level.player.running.get_busy():
                level.player.running.stop()
            return 'win'
        display.update()
        clock.tick(30)


# cur_state = 'menu', а взагалі є menu, rules, pause, level, win, loose, bonus
cur_state = 'bonus'
cur_level = 3
while run:  # switcher
    for e in event.get():
        if e.type == QUIT:
            run = False
    if cur_state == 'level':
        cur_state = level_play(True)
    elif cur_state == 'pause':
        cur_state = pause()
    elif cur_state == 'menu':
        cur_state = menu()
    elif cur_state == 'rules':
        cur_state = rules()
    elif cur_state == 'win':
        cur_state = level_complete('win')
    elif cur_state == 'loose':
        cur_state = level_complete('loose')
    elif cur_state == 'bonus':
        cur_state = bonus_level()
    else:
        cur_state = level_play(False)
