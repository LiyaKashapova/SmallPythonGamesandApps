from pygame import *

window = display.set_mode((700, 500))
display.set_caption("Догонялки")
background = transform.scale(image.load("C:\\Users\\13\\PycharmProjects\\Labirynth\\back.jpg"), (700, 500))

c = {
    's1': [100, 300],
    's2': [300, 300]
}

speed = 10

s1 = transform.scale(image.load('C:\\Users\\13\\PycharmProjects\\Labirynth\\monkey.png'), (100, 100))
s2 = transform.scale(image.load('C:\\Users\\13\\PycharmProjects\\Labirynth\\tiger.png'), (100, 100))


run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    keys_pressed = key.get_pressed()
    if keys_pressed[K_LEFT] and c['s1'][0] > 5:
        c['s1'][0] -= speed
    if keys_pressed[K_RIGHT] and c['s1'][0] < 595:
        c['s1'][0] += speed
    if keys_pressed[K_UP] and c['s1'][1] > 5:
        c['s1'][1] -= speed
    if keys_pressed[K_DOWN] and c['s1'][1] < 395:
        c['s1'][1] += speed
    if keys_pressed[K_a] and c['s2'][0] > 5:
        c['s2'][0] -= speed
    if keys_pressed[K_d] and c['s2'][0] < 595:
        c['s2'][0] += speed
    if keys_pressed[K_w] and c['s2'][1] > 5:
        c['s2'][1] -= speed
    if keys_pressed[K_s] and c['s2'][1] < 395:
        c['s2'][1] += speed
    window.blit(background, (0, 0))
    window.blit(s1, (c['s1'][0], c['s1'][1]))
    window.blit(s2, (c['s2'][0], c['s2'][1]))
    display.update()
    clock.tick(60)