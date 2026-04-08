from turtle import Turtle, Screen

ALIGNMENT = "center"
FONT = ('Arial', 25, 'normal')


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color(230,200,250)
        self.penup()
        #save highscore to remember it
        with open("snake_game2/score.txt") as data:
            self.highscore = str(data.read())
        self.goto(0,260)
        self.hideturtle()
        self.update_score()

    def update_score(self):
        self.write(f"Score: {self.score} Highscore: {self.highscore}", align=ALIGNMENT, font=FONT)
    #reset the scoreboard
    def reset(self):
        self.score = 0
        self.color(230,200,250)
        self.penup()        
        self.goto(0,260)
        self.hideturtle()
        self.update_score()            
    #game over pop-up
    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)  
        self.goto(0,-20)
        self.write("Press ''space'' to restart the game", align=ALIGNMENT, font=('Arial', 15, 'normal')) 
    #increase score and increase highscore 
    # if score is higher than highscore and save the highscore
    def increase_score(self):
        self.score +=1
        if self.score > int(self.highscore):
            self.highscore = self.score
            with open("snake_game2/score.txt", mode="w") as data:
                data.write(f"{self.highscore}")
        self.clear()
        self.update_score()