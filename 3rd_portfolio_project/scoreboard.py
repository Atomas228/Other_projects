from turtle import Turtle, Screen

ALIGNMENT = "center"
FONT = ('Arial', 35, 'bold')


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.x_score = 0
        self.o_score = 0
        self.penup()
        self.hideturtle()
    #updates the score
    def update_score(self):
        self.color(100, 127, 188)
        self.goto(0,260)
        self.write(f"X: {self.x_score}  O: {self.o_score}", align=ALIGNMENT, font=FONT)
    #resets the score
    def reset(self):
        self.penup()        
        self.hideturtle()
        self.update_score()            
    # text abot the ended game
    def game_over(self, winner):
        self.goto(0, 0)
        self.color(90, 117, 178)
        if winner == "tie":
            self.write(f"Its a tie", align=ALIGNMENT, font=FONT)  
        else:
            self.write(f"The {winner} player wins", align=ALIGNMENT, font=FONT)  
        self.goto(0,-20)
        self.write("Press ''space'' to restart the game", align=ALIGNMENT, font=('Arial', 20, 'normal'))
    #increases the score for every mark separately
    def increase_score(self, winner):
        if winner == "X":
            self.x_score +=1
        else:
            self.o_score +=1
        self.clear()
        self.update_score()         