from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, n, im, c, rx, ry, rw, rh, sx, sy):
        super().__init__()
        self.name = n
        self.image = im
        self.rect = Rect(rx, ry, rw, rh)
        self.rect.x = rx
        self.rect.y = ry
        self.sx = sx
        self.sy = sy
        self.color = c

    def draw(self):
        if self.image:
            w.blit(self.image, (self.rect.x + self.sx, self.rect.y + self.sy))
        draw.rect(w, self.color, self.rect, 3)


lred = (255, 69, 0)
red = (180, 0, 0)
lblue = (0, 206, 209)
blue = (30, 144, 255)
black = (0, 0, 0)
white = (245, 245, 245)

mixer.init()
files = {
    'Saitama': image.load('Saitama.png'),
    'Genos': image.load('Genos.png'),
    'Bang': image.load('Bang.png'),
    'Sonic': image.load('Sonic.png'),
    'Fubuki': image.load('Fubuki.png'),
    'Garou': image.load('Garou.png'),
    'icon': image.load('icon.png'),
    'button': image.load('button.png'),
    'button_grey': image.load('buttongrey.png'),
    'click': mixer.Sound('click.mp3'),
    'victory': mixer.Sound('victory.mp3'),
    'draw': mixer.Sound('draw.ogg')
}

sprites = {
    'Saitama': GameSprite('Saitama', transform.scale(files['Saitama'], (100, 200)), black, 0, 0, 200, 200, 50, 0),
    'Genos': GameSprite('Genos', transform.scale(files['Genos'], (200, 200)), black, 0, 200, 200, 200, 0, 0),
    'Bang': GameSprite('Bang', transform.scale(files['Bang'], (200, 200)), black, 0, 400, 200, 200, 0, 0),
    'Sonic': GameSprite('Sonic', transform.scale(files['Sonic'], (150, 200)), black, 400, 0, 200, 200, 20, 0),
    'Fubuki': GameSprite('Fubuki', transform.scale(files['Fubuki'], (100, 200)), black, 400, 200, 200, 200, 50, 0),
    'Garou': GameSprite('Garou', transform.scale(files['Garou'], (200, 200)), black, 400, 400, 200, 200, 0, 0),
    'default': GameSprite('default', None, black, 200, 0, 200, 200, 0, 0),
    'button': GameSprite('button', files['button'], black, 225, 440, 150, 100, 0, 0)
}

field = [[sprites['Saitama'], sprites['Genos'], sprites['Bang']],
         [sprites['default'], sprites['default'], sprites['default']],
         [sprites['Sonic'], sprites['Fubuki'], sprites['Garou']]]

ww = 600
wh = 600
w = display.set_mode((ww, wh))
display.set_caption('OPM Tic-Tac-Toe')
display.set_icon(files['icon'])
w.fill(white)

font.init()
f = font.SysFont('Impact', 35)
w.blit(f.render('Choose', True, red), (240, 120))
w.blit(f.render('Two', True, blue), (270, 170))
w.blit(f.render('Characters', True, red), (220, 220))
bn = f.render('Play', True, black)
sprites['button'].draw()
w.blit(bn, (270, 470))

files['click'].set_volume(0.4)
files['victory'].set_volume(0.4)
files['draw'].set_volume(0.4)

game = play = True
players = ['l', 'r']
clock = time.Clock()


def button_click():
    files['click'].play()
    global play
    sprites['button'].image = files['button_grey']
    sprites['button'].draw()
    w.blit(bn, (270, 470))
    display.update()
    time.delay(200)
    if players[0] != 'l' and players[1] != 'r':
        play = False
    else:
        sprites['button'].image = files['button']
        sprites['button'].draw()
        w.blit(bn, (270, 470))
        display.update()
        time.delay(200)


for fi in field:
    for i in fi:
        if i.name != 'default':
            i.draw()

while game and play:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            if x < 200:
                files['click'].play()
                for fi in field[0]:
                    if fi.rect.collidepoint(x, y):
                        fi.color = lred
                        players[0] = fi.name
                    else:
                        fi.color = black
                    fi.draw()
            elif x > 400:
                files['click'].play()
                for fi in field[2]:
                    if fi.rect.collidepoint(x, y):
                        fi.color = lblue
                        players[1] = fi.name
                    else:
                        fi.color = black
                    fi.draw()
            if sprites['button'].rect.collidepoint(x, y):
                button_click()
        clock.tick(60)
        display.update()


def draw_field():
    w.fill(white)
    y = 0
    for i in range(3):
        x = 0
        for j in range(3):
            s = sprites[field[i][j].name]
            field[i][j] = GameSprite(field[i][j].name, s.image, s.color, x, y, s.rect.width, s.rect.height, s.sx, s.sy)
            field[i][j].draw()
            x += 200
        y += 200


def check_win():
    for r in range(3):
        if field[r][0].name != 'default' and field[r][0].name == field[r][1].name == field[r][2].name:
            return field[r][0].name
        if field[0][r].name != 'default' and field[0][r].name == field[1][r].name == field[2][r].name:
            return field[0][r].name
    if field[0][0].name != 'default' and field[0][0].name == field[1][1].name == field[2][2].name:
        return field[0][0].name
    if field[2][0].name != 'default' and field[2][0].name == field[1][1].name == field[0][2].name:
        return field[2][0].name
    for r in range(3):
        for c in range(3):
            if field[r][c].name == 'default':
                return False
    return 'Draw'


play = True
player = 'left'
for i in range(3):
    for j in range(3):
        field[i][j].name = 'default'
draw_field()

while game and play:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            files['click'].play()
            x, y = e.pos
            for i in range(3):
                for j in range(3):
                    if field[i][j].rect.collidepoint(x, y) and field[i][j].name == 'default':
                        if player == 'left':
                            field[i][j].name = players[0]
                            player = 'right'
                        else:
                            field[i][j].name = players[1]
                            player = 'left'
            draw_field()
            c = check_win()
            if c == 'Draw':
                w.fill(white)
                lp, rp = sprites[players[0]], sprites[players[1]]
                w.blit(transform.scale(files[players[0]], (lp.image.get_width() * 2, lp.image.get_height() * 2)), (lp.sx, lp.sy + 130))
                w.blit(transform.scale(files[players[1]], (rp.image.get_width() * 2, rp.image.get_height() * 2)), (rp.sx + 300, rp.sy + 130))
                w.blit(f.render('Draw!', True, black), (270, 50))
                files['draw'].play()
            elif c:
                w.fill(white)
                i = sprites[c].image
                sx_add = 100
                if c == 'Saitama':
                    sx_add = 160
                elif c == 'Fubuki':
                    sx_add = 150
                w.blit(transform.scale(files[c], (i.get_width() * 2, i.get_height() * 2)), (sprites[c].sx + sx_add, sprites[c].sy + 130))
                w.blit(f.render('Here\'s our winner!', True, sprites[c].color), (180, 50))
                files['victory'].play()
    clock.tick(60)
    display.update()
