from turtle import Turtle, Screen

ALIGNMENT = "center"
FONT = ('Arial', 35, 'bold')


class Choose_game(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.player = 0
        self.game_level = 0
        #Checks where user clicks and finds what player(bot or PvP) user wants to play against
    def choose_player(self, x, y):
        if x in range(-65,-15) and y in range(-25,0):
            self.player = 2
        elif x in range(12, 65) and y in range(-25,0):   
            self.player = 1
        #Checks where user clicks and finds at what difficulty level (easy(1), medium(2), hard(3) player wants to play)
    def choose_level(self,x,y):
        if x in range(-170,-130) and y in range(-25,0):
            self.game_level = 1
        elif x in range(-30, 30) and y in range(-25, 0):
            self.game_level = 2
        elif x in range(130, 170) and y in range(-25, 0):
            self.game_level = 3
        # Pops out the question about either playing against other player or bot
    def first_question(self):
        self.goto(0, 30)
        self.color(90, 117, 178)
        self.write(f"Choose who do you want to play against?", align=ALIGNMENT, font=('Arial', 20, 'normal'))
        self.goto(-40, -30)
        self.write(f"1v1", align=ALIGNMENT, font=FONT)  
        self.goto(40, -30)
        self.write(f"Bot", align=ALIGNMENT, font=FONT)    
        #Pops out the question about the difficulty level 
    def second_question(self):
        self.goto(0, 30)
        self.color(90, 117, 178)
        self.write(f"Choose Level:", align=ALIGNMENT, font=('Arial', 20, 'normal'))
        self.goto(-150, -30)
        self.color(250, 253, 214)
        self.write(f"Easy", align=ALIGNMENT, font=FONT)  
        self.goto(0, -30)
        self.color(145, 173, 200)
        self.write(f"Medium", align=ALIGNMENT, font=FONT)         
        self.goto(150, -30)
        self.color(100, 127, 188)
        self.write(f"Hard", align=ALIGNMENT, font=FONT)