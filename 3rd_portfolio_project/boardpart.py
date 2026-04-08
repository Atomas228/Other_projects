from turtle import Turtle, Screen
#Creates the board
class Board(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.grid = Turtle()
        self.grid.hideturtle()
        self.grid.color(145, 173, 200)
        self.grid.speed(0)
        self.grid.pensize(14)
#every block does the line
    def create_board(self):
        self.grid.penup()
        self.grid.goto(-100, 300)
        self.grid.pendown()
        self.grid.goto(-100, -300)

        self.grid.penup()
        self.grid.goto(100, 300)
        self.grid.pendown()
        self.grid.goto(100, -300)

        self.grid.penup()
        self.grid.goto(-300, 100)
        self.grid.pendown()
        self.grid.goto(300, 100)

        self.grid.penup()
        self.grid.goto(-300, -100)
        self.grid.pendown()
        self.grid.goto(300, -100)
        self.screen.update()
