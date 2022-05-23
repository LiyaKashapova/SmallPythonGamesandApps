import pygame
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Key:
    def __init__(self, cx=0, cy=0):
        self.rect = pygame.Rect(cx, cy, 50, 100)

    def draw(self):
        pygame.draw.rect(w, (255, 255, 255), self.rect)
        pygame.draw.rect(w, (0, 0, 0), self.rect, 10)

    def collide(self, cx, cy):
        return self.rect.collidepoint(cx, cy)


pygame.init()
w = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Small Piano')
pygame.display.set_icon(pygame.image.load(resource_path('piano.png')))
w.fill((152, 251, 152))
font = pygame.font.SysFont('monotype corsiva', 60)
notes = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'Lya', 'Si']
notess = [pygame.mixer.Sound(resource_path('do.mp3')), pygame.mixer.Sound(resource_path('re.mp3')),
          pygame.mixer.Sound(resource_path('mi.mp3')), pygame.mixer.Sound(resource_path('fa.mp3')),
          pygame.mixer.Sound(resource_path('sol.mp3')), pygame.mixer.Sound(resource_path('lya.mp3')),
          pygame.mixer.Sound(resource_path('si.mp3'))]
sound = pygame.image.load(resource_path('sound.png'))
clock = pygame.time.Clock()

keys = []
x = 20
for i in range(7):
    key = Key(x, 170)
    keys.append(key)
    x += 70

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(len(keys)):
                if keys[i].collide(x, y):
                    notess[i].play()
                    cn = font.render(notes[i], True, (0, 0, 0))
        else:
            cn = font.render(' ', True, (0, 0, 0))
    w.fill((152, 251, 152))
    for i in range(7):
        keys[i].draw()
    w.blit(font.render('Thats a small piano!', True, (0, 0, 0)), (30, 50))
    w.blit(sound, (30, 250))
    w.blit(cn, (300, 340))
    pygame.display.update()
    clock.tick(40)
