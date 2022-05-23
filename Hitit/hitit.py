from turtle import *

width = 200
height = 180

class Sprite(Turtle):
    def __init__(self, x, y, step=20, shape='circle', color='black'):
        Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.color(color)
        self.shape(shape)
        self.step = step
        self.points = 0

    def mup(self):
        self.goto(self.xcor(), self.ycor() + self.step)

    def mdown(self):
        self.goto(self.xcor(), self.ycor() - self.step)

    def mleft(self):
        self.goto(self.xcor() - self.step, self.ycor())

    def mright(self):
        self.goto(self.xcor() + self.step, self.ycor())

    def is_collide(self, sprite):
        if self.distance(sprite.xcor(), sprite.ycor()) < 30:
            return True
        else:
            return False

    def set_move(self, x_start, y_start, x_end, y_end):
        self.x_s = x_start
        self.y_s = y_start
        self.x_e = x_end
        self.y_e = y_end
        self.goto(x_start, y_start)
        self.setheading(self.towards(x_end, y_end))

    def make_step(self):
        self.forward(self.step)
        if self.distance(self.x_e, self.y_e) < self.step:
            self.set_move(self.x_e, self.y_e, self.x_s, self.y_s)


player = Sprite(0, -100, 25, 'circle', 'orange')
enemy1 = Sprite(-width, 0, 10, 'square', 'red')
enemy1.set_move(-width, 0, width, 0)
enemy2 = Sprite(width, 70, 10, 'square', 'red')
enemy2.set_move(width, 100, -width, 100)
prize = Sprite(0, 150, 20, 'triangle', 'green')

scr = player.getscreen()
scr.listen()
scr.onkey(player.mup, 'w')
scr.onkey(player.mleft, 'a')
scr.onkey(player.mright, 'd')
scr.onkey(player.mdown, 's')
points = 0
while points < 3:
    enemy1.make_step()
    enemy2.make_step()
    if player.is_collide(prize):
        points += 1
        player.goto(0, -100)
    if player.is_collide(enemy1) or player.is_collide(enemy2):
        prize.hideturtle()
        break
if points == 3:
    enemy1.hideturtle()
    enemy2.hideturtle()
