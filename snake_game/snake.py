from turtle import Turtle

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
#starting position of snake head and its segments
start_pos = [(0,0),(-20,0),(-40,0)]

class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        self.can_turn = True
        self.wall = Turtle()
        self.wall.pensize(10)
        self.wall.color(123,50,0)
        self.wall.penup()
        self.wall.hideturtle()
        self.wall.goto(-296,296)
        self.wall.pendown()
        #create a wall and make the borders almost at the 300 x_axis and y_axis
        self.wall.goto(296,296)
        self.wall.goto(296,-295)
        self.wall.goto(-296,-296)
        self.wall.goto(-296,296)

    def create_snake(self):
        for position in start_pos:
            self.add_segment(position)
    #reset the snake segments
    def reset(self):
        for seg in self.segments:
            seg.hideturtle()
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]

    #add a segment to last snake's segment
    def add_segment(self, position):
        new_segment = Turtle("square")
        new_segment.speed(1)
        new_segment.color(230,245,200)
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    #add the segment at the
    def extend(self):
        self.add_segment(self.segments[-1].position())        

    #make snake segments turn together with its head and forward 20
    def move(self):
        for seg in range(len(self.segments)-1, 0, -1):
            new_x = self.segments[seg - 1].xcor()
            new_y = self.segments[seg - 1].ycor()
            self.segments[seg].goto(new_x,new_y)
            self.can_turn = True
        self.head.forward(20)
        
    #cant turn backwards and cant turn twice in the same place
    def up(self):
        if self.can_turn and self.head.heading() != DOWN:
            self.segments[0].setheading(UP)
            self.can_turn = False
    def down(self):
        if self.can_turn and self.head.heading() != UP:
            self.segments[0].setheading(DOWN)
            self.can_turn = False
    def left(self):
        if self.can_turn and self.head.heading() != RIGHT:
            self.segments[0].setheading(LEFT)
            self.can_turn = False
    def right(self):
        if self.can_turn and self.head.heading() != LEFT:
            self.segments[0].setheading(RIGHT)
            self.can_turn = False