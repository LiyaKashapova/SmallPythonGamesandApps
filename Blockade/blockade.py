from pygame import *

images = {
    'back': transform.scale(image.load('images/background.png'), (1280, 720)),
    'player': transform.scale(image.load("images/player.png"), (50, 50)),
    'enemy': transform.scale(image.load("images/robot.png"), (50, 50)),
    'crystal': transform.scale(image.load("images/crystal.png"), (50, 50)),
    'obs': transform.scale(image.load("images/obs.png"), (40, 120)),
    'key': transform.scale(image.load("images/key.png"), (40, 50)),
    'chest_opened': transform.scale(image.load("images/chest/chest4.png"), (80, 60)),
    'chest_closed': transform.scale(image.load("images/chest/chest1.png"), (80, 60)),
    'stair': transform.scale(image.load("images/stair.png"), (40, 180)),
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
strike_sound, kick_sound, key_sound, crystal_sound, obs_sound, teleport_sound, click_sound, chest_sound, game_sound, \
    menu_sound, end_sound = mixer.Sound('sounds/strike.mp3'), mixer.Sound('sounds/lasers.mp3'),\
    mixer.Sound('sounds/backpack.mp3'), mixer.Sound('sounds/crystal.mp3'), mixer.Sound('sounds/remove.mp3'),\
    mixer.Sound('sounds/teleport.wav'), mixer.Sound('sounds/click.wav'), mixer.Sound('sounds/metal.mp3'),\
    mixer.Sound('sounds/game.mp3'), mixer.Sound('sounds/menu.mp3'), mixer.Sound('sounds/game_over.wav')
crystal_sound.set_volume(0.3)


class GameSprite(sprite.Sprite):
    def __init__(self, x, y, i, speed=0):
        super().__init__()
        self.image = i
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.speed = speed

    def update(self, camera):
        w.blit(self.image, camera.apply(self))


class Player(GameSprite):
    strikes = sprite.Group()
    holding = False

    def __init__(self, x, y, img, speed, side):
        GameSprite.__init__(self, x, y, img, speed)
        self.side = side

    def move_x(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
            self.image = transform.flip(images['player'], True, False)
            self.side = 'left'
        if keys[K_d]:
            self.rect.x += self.speed
            self.image = images['player']
            self.side = 'right'

    def move_y(self, stair):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if self.rect.y <= (stair.rect.y - 40):
            self.rect.y = stair.rect.y - 40
        if self.rect.y >= (stair.rect.y + 130):
            self.rect.y = stair.rect.y + 130

    def update(self, camera):
        for e in event.get():
            if e.type == KEYDOWN and e.key == K_SPACE and not self.holding:
                self.holding = True
                self.strikes.add(Strike(self.rect.centerx, self.rect.centery - 10, images['strike'], 3, self.side))
                strike_sound.play()
            elif e.type == KEYUP and e.key == K_SPACE:
                self.holding = False
        self.strikes.update(camera)
        w.blit(self.image, camera.apply(self))


class Strike(GameSprite):
    def __init__(self, x, y, img, speed, side):
        GameSprite.__init__(self, x, y, img, speed)
        self.side = side

    def update(self, camera):
        if self.side == 'right':
            self.rect.x += self.speed
        if self.side == 'left':
            self.rect.x -= self.speed
        w.blit(self.image, camera.apply(self))


class Enemy(GameSprite):
    def __init__(self, x, y, img, speed, side):
        GameSprite.__init__(self, x, y, img, speed)
        self.side = side

    def update(self, camera):
        if self.side == 'right':
            self.rect.x += self.speed
        if self.side == 'left':
            self.rect.x -= self.speed
        w.blit(self.image, camera.apply(self))


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
f, f2, f3 = font.Font('fonts/LifeForm.ttf', 200),\
            font.Font('fonts/Surfing Capital.ttf', 60), font.Font('fonts/mrsmonstercond.ttf', 45)
white = (255, 255, 255)


class Level:
    level = []
    level_width, level_height, crystal_count, chest_key, obs_key = 0, 0, 0, False, False
    platforms, block_r, block_l, enemies = sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()
    stairs, crystals, chest_keys, chests, obs = sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group(), sprite.Group()
    portal = sprite.Sprite()
    mes = {'e_chest': f2.render('Press E to pick the chest key!', True, white),
           'e_look': f2.render('Press E to look for the antigraviton!', True, white),
           'e_open': f2.render('Press E to remove the gravitational trap!', True, white),
           'key_chest': f2.render('You need a key to open the chest!', True, white),
           'key_obs': f2.render('You need a key to remove the trap!', True, white),
           'space': f2.render('Press SPACE to shoot lasers', True, white)
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
            if sprite.spritecollide(en, self.block_r, False):  # flip enemies to left if they reached the right side
                en.side = 'left'
                en.image = transform.flip(images['enemy'], True, False)
            elif sprite.spritecollide(en, self.block_l, False):  # flip enemies to right if they reached the left side
                en.side = 'right'
                en.image = images['enemy']
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
                self.player.move_y(s)
            s.update(self.camera)
        for c in self.crystals:  # drawing crystals
            if sprite.collide_rect(self.player, c):  # collecting crystals
                crystal_sound.play()
                self.crystal_count += 1
                c.kill()
            if c:
                c.update(self.camera)
        keys = key.get_pressed()
        for k in self.chest_keys:  # drawing chest keys
            if sprite.collide_rect(self.player, k):  # collecting chest keys
                w.blit(self.mes['e_chest'], ((ww - self.mes['e_chest'].get_width()) / 2, 50))
                if keys[K_e]:
                    key_sound.play()
                    k.kill()
                    self.chest_key = True
            if k:
                k.update(self.camera)
        for c in self.chests:  # drawing chests
            # opening chests to collect crystals & antigravitons
            if sprite.collide_rect(self.player, c) and not self.obs_key:
                if not self.chest_key:
                    w.blit(self.mes['key_chest'], ((ww - self.mes['key_chest'].get_width()) / 2, 50))
                elif not self.obs_key:
                    w.blit(self.mes['e_look'], ((ww - self.mes['e_look'].get_width()) / 2, 50))
                    if keys[K_e]:
                        chest_sound.play()
                        c.image = images['chest_opened']
                        self.crystal_count += 10
                        self.obs_key, self.chest_key = True, False
                print('key: ', c, 'amount: ', len(self.chests))
            c.update(self.camera)
        for o in self.obs:  # drawing obs
            if sprite.collide_rect(self.player, o):  # removing obs
                if not self.obs_key:
                    w.blit(self.mes['key_obs'], ((ww - self.mes['key_obs'].get_width()) / 2, 50))
                    self.player.rect.x = o.rect.x - 50
                else:
                    w.blit(self.mes['e_open'], ((ww - self.mes['e_open'].get_width()) / 2, 50))
                    self.player.rect.x = o.rect.x - 50
                    if keys[K_e]:
                        obs_sound.play()
                        o.kill()
                        self.obs_key = False
                print('key: ', o, 'amount: ', len(self.obs))
            if o:
                o.update(self.camera)
        self.portal.update(self.camera)
        if sprite.spritecollide(self.player, self.platforms, False) \
                and not sprite.spritecollide(self.player, self.block_r, False) \
                and not sprite.spritecollide(self.player, self.block_l, False):
            self.player.move_x()
        self.player.update(self.camera)
        return flag


class Level1(Level):
    level = [
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l                                                                    r",
        "l l   °  °     r               l            l   °  °  °     r       r",
        "l  ------------                  -------      ---------------        r",
        "l l | r                             l | r    l | r       l | r       r",
        "l l   r                             l   r    l   r       l   r       r",
        "l l    °nr                          l     °  °   r    l      r       r",
        "l  ------                            ------------      -------       r",
        "l     l | r                                          l | r           r",
        "l     l   r                                          l   r           r",
        "l     l       °  °  r                         l °  °     r           r",
        "l      -------------                           ---------             r",
        "l               l | r                         l | r                  r",
        "l               l   r                         l   r                  r",
        "l                                                                    r",
        "----------------------------------------------------------------------"]
    level_width = len(level[0]) * 40
    level_height = len(level) * 40

    def __init__(self):
        player = Player(300, 650, images['player'], 10, 'right')
        super().__init__(player)
        self.enemies.add(Enemy(400, 480, images['enemy'], 3, 'right'), Enemy(230, 320, images['enemy'], 3, 'right'),
                         Enemy(1800, 160, images['enemy'], 3, 'right'), Enemy(1700, 320, images['enemy'], 3, 'right'))
        self.obs.add(GameSprite(1000, 580, images['obs']), GameSprite(2600, 580, images['obs']))
        self.chest_keys.add(GameSprite(210, 340, images['key']), GameSprite(1600, 340, images['key']))
        self.chests.add(GameSprite(450, 150, images['chest_closed']),
                        GameSprite(1400, 150, images['chest_closed']))
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
        "l  l     °         °           °            r       l               rr",
        "l   ----------------------------------------         --------------- r",
        "l  l | r                              l | r              l | r       r",
        "l  l   r                              l   r              l   r       r",
        "l l              r              l   °        °        °       r      r",
        "l  --------------                -----------------------------       r",
        "l                                l | r                               r",
        "l                                l   r                               r",
        "l    l       °       °             °      °                  r       r",
        "l     -------------------------------------------------------        r",
        "l                   l | r                                l | r       r",
        "l                   l   r                                l   r       r",
        "l          °                    °       °            °               r",
        "----------------------------------------------------------------------"]
    level_width = len(level[0]) * 40
    level_height = len(level) * 40

    def __init__(self):
        player = Player(300, 810, images['player'], 10, 'right')
        super().__init__(player)
        self.enemies.add(Enemy(400, 640, images['enemy'], 3, 'right'), Enemy(230, 320, images['enemy'], 3, 'right'),
                         Enemy(1800, 160, images['enemy'], 3, 'right'), Enemy(1700, 320, images['enemy'], 3, 'right'),
                         Enemy(1700, 480, transform.flip(images['enemy'], True, False), 3, 'left'),
                         Enemy(1700, 640, transform.flip(images['enemy'], True, False), 3, 'left'),
                         Enemy(230, 480, images['enemy'], 3, 'right'))
        self.obs.add(GameSprite(1700, 410, images['obs']), GameSprite(1000, 100, images['obs']))
        self.chest_keys.add(GameSprite(2350, 500, images['key']), GameSprite(600, 500, images['key']))
        self.chests.add(GameSprite(250, 640, images['chest_closed']))
        self.portal = GameSprite(100, 100, images['portal'])


class Button:
    def __init__(self, line_xy, t, bw=470, bh=70, c=(106, 90, 205), t_color=(255, 255, 255)):
        self.image = Surface([bw, bh])
        self.image.fill(c)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.y = line_xy[0], line_xy[1]
        self.text = f2.render(t, True, t_color)

    def draw(self, shift_x=None, shift_y=5):
        if not shift_x:
            shift_x = (self.rect.width - self.text.get_width()) / 2
        w.blit(self.image, (self.rect.x, self.rect.y))
        w.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))


run = True
clock = time.Clock()
cur_level, level = 1, None

magenta, red, purple = (150, 0, 150), (178, 34, 34), (106, 90, 205)
game_header, pause_header = f.render("BLOCKADE", True, white, red), f.render("PAUSE", True, white, red)
xy = [((ww - game_header.get_width()) / 2, 70), (ww / 2, 300), (ww / 2, 450), (ww / 2, 600)]


def rules():
    global run
    elements = [game_header, f3.render('Move with WASD. You can only go up and down the stairs.', True, magenta),
                f3.render('Move with WASD. You can only go up and down the stairs.', True, purple),
                f3.render('Use SPACE to shoot. Use E to interact with the world.', True, magenta),
                f3.render('Use SPACE to shoot. Use E to interact with the world.', True, purple),
                Button(xy[3], 'BACK TO MENU')]
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
        w.blit(elements[0], xy[0])  # header
        # background for rules
        draw.rect(w, white, Rect((ww - elements[1].get_width()) / 2 - 50, xy[1][1] - 10, elements[1].get_width() + 100,
                                 (elements[1].get_height() + elements[3].get_height()) + 130))
        w.blit(elements[1], ((ww - elements[1].get_width()) / 2, xy[1][1]))
        w.blit(elements[2], (((ww - elements[1].get_width()) / 2) - 3, xy[1][1]))
        w.blit(elements[3], ((ww - elements[3].get_width()) / 2, xy[2][1]))
        w.blit(elements[4], (((ww - elements[3].get_width()) / 2) - 3, xy[2][1]))
        elements[5].draw()
        display.update()
        clock.tick(30)


def menu():
    global run
    elements = [game_header, Button(xy[1], 'START GAME'), Button(xy[2], 'HOW TO PLAY'), Button(xy[3], 'EXIT GAME')]
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
        w.blit(elements[0], xy[0])  # header
        for i in range(1, 4):  # buttons
            elements[i].draw()
        display.update()
        clock.tick(30)


def level_play(restart=True):
    global run, cur_level, level
    if restart:
        level = Level1() if cur_level == 1 else Level2()
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
                    return 'pause'
        w.blit(images['back'], (0, 0))
        if not level.update():
            return 'loose'
        w.blit(transform.scale(images['crystal'], (50, 50)), (10, 10))  # updating crystals' counter
        w.blit(f3.render(f': {level.crystal_count}', True, white), (60, 10))
        btn_pause.draw(0, -10)
        if sprite.collide_rect(level.player, level.portal):
            return 'win'
        display.update()
        clock.tick(30)


def pause():
    global run, pause_header
    elements = [pause_header, Button(xy[1], 'CONTINUE'), Button(xy[2], 'RESTART'), Button(xy[3], 'BACK TO MENU')]
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
        w.blit(elements[0], ((ww - pause_header.get_width()) / 2, xy[0][1]))  # header
        for i in range(1, 4):  # buttons
            elements[i].draw()
        display.update()
        clock.tick(30)


def level_complete(result):
    global run, cur_level, level
    game_state = 0  # 0 - level was completed, 1 - won, 2 - lost
    if result == 'win' and cur_level == 2:
        game_state = 1
    elif result == 'loose':
        game_state = 2
        music.play(end_sound, -1)
    teleport_sound.play()
    level.clear()
    headers = [f.render("LEVEL DONE", True, purple, red), f.render("YOU WON", True, purple, red),
               f.render("YOU LOST", True, purple, red)]
    elements = []
    if not game_state:
        elements = [Button(xy[1], 'RESTART'), Button(xy[2], 'NEXT LEVEL'), Button(xy[3], 'BACK TO MENU')]
    else:
        elements = [Button(xy[1], 'RESTART'), Button(xy[2], 'HOW TO PLAY'), Button(xy[3], 'BACK TO MENU')]
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
        w.blit(headers[game_state], ((ww - headers[game_state].get_width()) / 2, xy[0][1]))  # header
        for i in range(0, 3):  # buttons
            elements[i].draw()
        display.update()
        clock.tick(30)


cur_state = 'menu'
while run:  # switcher
    for e in event.get():
        if e.type == QUIT:
            run = False
    if cur_state == 'menu':
        cur_state = menu()
    elif cur_state == 'rules':
        cur_state = rules()
    elif cur_state == 'pause':
        cur_state = pause()
    elif cur_state == 'level':
        cur_state = level_play(True)
    elif cur_state == 'win':
        cur_state = level_complete('win')
    elif cur_state == 'loose':
        cur_state = level_complete('loose')
    else:  # continue after pause
        cur_state = level_play(False)
