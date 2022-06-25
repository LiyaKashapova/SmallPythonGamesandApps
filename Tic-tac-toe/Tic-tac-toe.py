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
    'default': GameSprite('rect', None, black, 200, 0, 200, 200, 0, 0),
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
        if i.name != 'rect':
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
            name = field[i][j].name
            field[i][j] = GameSprite(name, files[name].image, sprites[name].color, x, y, sprites[name].rect.width,
                                     sprites[name].rect.height, sprites[name].sx, sprites[name].sy)
            field[i][j].draw()
            x += 200
        y += 200


def check_win():
    for i in range(3):
        if field[i][0].name != 'default' and field[i][0].name == field[i][1].name == field[i][2].name:
            return field[i][0].name
        if field[0][i].name != 'default' and field[0][i].name == field[1][i].name == field[2][i].name:
            return field[0][i].name
    if field[0][0].name != 'default' and field[0][0].name == field[1][1].name == field[2][2].name:
        return field[0][0].name
    if field[2][0].name != 'default' and field[2][0].name == field[1][1].name == field[0][2].name:
        return field[2][0].name
    for i in range(3):
        for j in range(3):
            if field[i][j].name == 'default':
                return False
    return 'Draw'


play = True
player = 0
for i in range(3):
    for j in range(3):
        field[i][j].name = 'default'
draw_field()

while game and play:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            files['click'].play()
            x, y = e.pos
            for i in range(3):
                for j in range(3):
                    if field[i][j].rect.collidepoint(x, y) and field[i][j].name == 'default':
                        if player == 0:
                            field[i][j].name = players[0]
                            player = 1
                        else:
                            field[i][j].name = players[1]
                            player = 0
            draw_field()
            c = check_win()
            if c == 'Draw':
                w.fill(white)
                w.blit(transform.scale(image.load(files[players[0]]),
                                       (sprites[players[0]].image.get_width() * 2,
                                        sprites[players[0]].image.get_height() * 2)),
                       (0 + sprites[players[0]].sx, 130 + sprites[players[0]].sy))
                w.blit(transform.scale(image.load(files[players[1]]),
                                       (sprites[players[1]].image.get_width() * 2,
                                        sprites[players[1]].image.get_height() * 2)),
                       (300 + sprites[players[1]].sx, 130 + sprites[players[1]].sy))
                w.blit(f.render('Draw!', True, black), (270, 50))
                files['draw'].play()
            elif c:
                w.fill(white)
                i = sprites[c].image
                if c == 'Saitama':
                    w.blit(transform.scale(image.load(files[c]), (i.get_width() * 2, i.get_height() * 2)),
                           (150 + sprites[c].sx, 130 + sprites[c].sy))
                else:
                    w.blit(transform.scale(image.load(files[c]), (i.get_width() * 2, i.get_height() * 2)),
                           (100 + sprites[c].sx, 130 + sprites[c].sy))
                w.blit(f.render('Here\'s our winner!', True, sprites[c].color), (180, 50))
                files['victory'].play()
        clock.tick(60)
        display.update()
