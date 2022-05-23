import turtle
import random

ww = 500
wh = 500

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}


def reset():
    global scor, dir, fcor, sseg
    scor = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    dir = "up"
    fcor = fpos()
    food.goto(fcor)
    move_snake()


def move_snake():
    global dir
    new_head = scor[-1].copy()
    new_head[0] = scor[-1][0] + offsets[dir][0]
    new_head[1] = scor[-1][1] + offsets[dir][1]
    if new_head in scor[:-1]:  # if we lost and new head is the end
        reset()
    else:
        scor.append(new_head)
        if not food_collision():
            scor.pop(0)
        if scor[-1][0] > ww / 2:
            scor[-1][0] -= ww
        elif scor[-1][0] < - ww / 2:
            scor[-1][0] += ww
        elif scor[-1][1] > wh / 2:
            scor[-1][1] -= wh
        elif scor[-1][1] < -wh / 2:
            scor[-1][1] += wh
        sseg.clearstamps()
        for segment in scor:
            sseg.goto(segment[0], segment[1])
            sseg.stamp()
        screen.update()
        turtle.ontimer(move_snake, 100)  # delay = 100 mlsec


def food_collision():
    global fcor
    if get_distance(scor[-1], fcor) < 20:
        fcor = fpos()
        food.goto(fcor)
        return True
    return False


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


def fpos():
    x = random.randint(-ww / 2 + 10, ww / 2 - 10)  # food size = 10 px
    y = random.randint(-wh / 2 + 10, wh / 2 - 10)
    return x, y



def go_up():
    global dir
    dir = "up"


def go_down():
    global dir
    dir = "down"


def go_right():
    global dir
    dir = "right"


def go_left():
    global dir
    dir = "left"


screen = turtle.Screen()
screen.setup(ww, wh)
screen.title("Snake")
screen.bgcolor('#90EE90')
screen.tracer(0)  # for smooth animation

sseg = turtle.Turtle("circle")
sseg.color('green')
sseg.penup()

food = turtle.Turtle()
food.shape("circle")
food.color('#800000')
food.shapesize(10 / 20)  # size of turtle is 20
food.penup()

screen.listen()
screen.onkey(go_up, "w")
screen.onkey(go_right, "d")
screen.onkey(go_down, "s")
screen.onkey(go_left, "a")

reset()
turtle.done()
