from turtle import Turtle
import random

class Food(Turtle):
    #create food
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.6, stretch_wid=0.6)
        self.color(200,40,30)
        self.speed("fastest")
        self.refresh()
    #refresh and move the food to some other random location
    def refresh(self):
        rand_x = random.randint(-280,280)
        rand_y = random.randint(-280,280)
        self.goto(rand_x, rand_y)