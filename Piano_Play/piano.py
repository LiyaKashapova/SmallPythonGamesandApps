import play
import pygame

play.set_backdrop('light blue')
text1 = play.new_text(words='Piano for fun!', x=0, y=200)
text2 = play.new_text(words='Create your melody by pressing the keys', x=0, y=150)

kp_m = play.new_box(color='light green', border_color='black', border_width=1, x=-100, y=-170, width=160, height=50)
kpm = play.new_text(words='Play melody', x=-100, y=-170, font_size=20)

kc_m = play.new_box(color='light yellow', border_color='black', border_width=1, x=100, y=-170, width=160, height=50)
kcm = play.new_text(words='Clear melody', x=100, y=-170, font_size=20)
sc_m = pygame.mixer.Sound('clear_melody.wav')

keys = []
sounds = []
melody = []

for i in range(8):
    kx = -180 + i * 50  # 40 - ширина, 10 - простір між клавішами
    key = play.new_box(color='white', border_color='black', border_width=3, x=kx, y=0, width=40, height=100)
    sound = pygame.mixer.Sound(str(i + 1) + '.ogg')
    keys.append(key)
    sounds.append(sound)


@play.when_program_starts
def start():
    pygame.mixer_music.load('hello.mp3')
    pygame.mixer_music.play()


@kc_m.when_clicked
def clear():
    melody.clear()
    sc_m.play()


@kp_m.when_clicked
async def play_m():
    for kp in range(len(sounds)):
        await play.timer(seconds=0.5)
        sounds[melody[kp]].play()


@play.repeat_forever
async def play_piano():
    for pr in range(len(keys)):
        if keys[pr].is_clicked:
            keys[pr].color = 'light grey'
            sounds[pr].play()
            await play.timer(seconds=0.3)
            keys[pr].color = 'white'
            melody.append(pr)


play.start_program()
