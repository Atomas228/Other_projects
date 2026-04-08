from turtle import Turtle, Screen

class Osandxs(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.mark = Turtle()
        self.mark.hideturtle()
        self.mark.color(145, 173, 200)
        self.mark.pensize(14)
        self.mark.penup()
    #draws O mark
    def draw_os(self, x_axis, y_axis):
        self.mark.goto(x_axis, y_axis)
        self.mark.pendown()
        self.mark.circle(75)
        self.mark.penup()
        self.screen.update()
    #draws X mark
    def draw_xs(self, x_axis, y_axis):
        self.mark.goto(x_axis-75, y_axis-75)
        self.mark.pendown()
        self.mark.goto(x_axis + 75,y_axis + 75)
        self.mark.penup()
        self.mark.goto(x_axis - 75, y_axis + 75)
        self.mark.pendown()
        self.mark.goto(x_axis + 75, y_axis - 75)
        self.mark.penup()
        self.screen.update()

