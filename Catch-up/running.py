from pygame import *

ww, wh = 700, 500
window = display.set_mode((ww, wh))
display.set_caption("Catch-Up")
display.set_icon(transform.scale(image.load('icon.png'), (50, 100)))
background = transform.scale(image.load("back.png"), (700, 500))

c = {
    's1': [100, 300],
    's2': [300, 300]
}

speed = 10

s1 = transform.scale(image.load('Saitama.png'), (100, 200))
s2 = transform.scale(image.load('Tatsumaki.png'), (100, 150))


run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    keys_pressed = key.get_pressed()
    if keys_pressed[K_LEFT] and c['s1'][0] > speed:
        c['s1'][0] -= speed
    if keys_pressed[K_RIGHT] and c['s1'][0] < ww - (speed + s1.get_width()):
        c['s1'][0] += speed
    if keys_pressed[K_UP] and c['s1'][1] > speed:
        c['s1'][1] -= speed
    if keys_pressed[K_DOWN] and c['s1'][1] < wh - (speed + s1.get_height()):
        c['s1'][1] += speed
    if keys_pressed[K_a] and c['s2'][0] > speed:
        c['s2'][0] -= speed
    if keys_pressed[K_d] and c['s2'][0] < ww - (speed + s2.get_width()):
        c['s2'][0] += speed
    if keys_pressed[K_w] and c['s2'][1] > speed:
        c['s2'][1] -= speed
    if keys_pressed[K_s] and c['s2'][1] < wh - (speed + s2.get_height()):
        c['s2'][1] += speed
    window.blit(background, (0, 0))
    window.blit(s1, (c['s1'][0], c['s1'][1]))
    window.blit(s2, (c['s2'][0], c['s2'][1]))
    display.update()
    clock.tick(60)