from pygame import *


class Key:
    def __init__(self, cx, cy):
        self.rect = Rect(cx, cy, 50, 100)

    def draw(self, win):
        draw.rect(win, (255, 255, 255), self.rect)
        draw.rect(win, (0, 0, 0), self.rect, 10)


init()
w = display.set_mode((500, 500))
display.set_caption('Small Piano')
display.set_icon(image.load('piano.png'))
sound = image.load('sound.png')
f = font.SysFont('monotype corsiva', 60)
n = f.render('That\'s a Small Piano', True, (0, 0, 0))
notes = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'Lya', 'Si']
notes_s = [mixer.Sound('do.mp3'), mixer.Sound('re.mp3'), mixer.Sound('mi.mp3'), mixer.Sound('fa.mp3'),
           mixer.Sound('sol.mp3'), mixer.Sound('lya.mp3'), mixer.Sound('si.mp3')]

keys = []
x = 20
for i in range(7):
    keys.append(Key(x, 170))
    x += 70

game = True
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            for i in range(len(keys)):
                if keys[i].rect.collidepoint(x, y):
                    notes_s[i].play()
                    cn = f.render(notes[i], True, (0, 0, 0))
        else:
            cn = f.render(' ', True, (0, 0, 0))
        w.fill((152, 251, 152))
        for i in range(7):
            keys[i].draw(w)
        w.blit(n, (30, 50))
        w.blit(cn, (300, 340))
        w.blit(sound, (30, 250))
        display.update()
        clock.tick(60)
