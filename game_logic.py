from turtle import Turtle, Screen
import random

class Game_logic(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        #Counts every move of players or a bot to decide what mark to put and which side plays now
        self.interaction = 0
        self.game_on = True
        #A list where X moves are added up to
        self.x_tries = []
        #A list where O moves are added up to
        self.o_tries = []
        # X_axis ranges of every cell to decide which cell is it
        self.ranges_x = [[-295,-105],[-95,95],[105,295],[-295,-105],[-95,95],[105,295],[-295,-105],[-95,95],[105,295]]
        # Y_axis ranges of every cell to decide which cell is it
        self.ranges_y = [[105,295],[105,295],[105,295],[-95,95],[-95,95],[-95,95],[-295,-105],[-295,-105],[-295,-105]]
        # Exact locations of every mark in the cells,
        # 1st is x_axis for both X and O, 2nd is y_axis for X mark,
        # 3rd is y_axis for O mark
        self.x_y_axis = [[-200,200,125],[0,200,125],[200,200,125],[-200,0,-75],[0,0,-75],[200,0,-75],[-200,-200,-275],[0,-200,-275],[200,-200,-275]]
        #Every possible combination of cells to win the game
        self.winning_combos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        #Booleans to show which side won
        self.x_wins = False
        self.o_wins = False
        self.draw = False
        self.input_locked = False

        #Reset method to reset all the variables for the new game
    def reset(self):
        self.x_tries = []
        self.o_tries = []     
        self.draw = False
        self.interaction = 0
        self.game_on = True
        self.input_locked = False

        #Move handler for PvP 
    def move_handler(self, x, y):
        #Dont run the method if the game is already done
        if not self.game_on:
            return
        #Loops through each cell
        for i in range(9):
            #If condition for x_axis and y_axis to select the cell
            if x in range(int(self.ranges_x[i][0]),int(self.ranges_x[i][1])) and y in range(int(self.ranges_y[i][0]),int(self.ranges_y[i][1])):
                #if condition to check if the cell is not already taken
                if i not in self.o_tries and i not in self.x_tries:
                    self.interaction += 1
                    #if else condition to determine which mark to put and what player is now playing
                    if self.interaction % 2 == 0:
                        self.o_tries.append(i)
                        self.winner_checker()
                        return 'O', self.x_y_axis[i][0], self.x_y_axis[i][2]
                    else:
                        self.x_tries.append(i)
                        self.winner_checker()
                        return 'X', self.x_y_axis[i][0], self.x_y_axis[i][1]
        #return none if nothing is found
        return None, None, None
    
    #finding available spots in a lop
    def available_spots(self):
        return [n for n in range(9) if n not in self.o_tries + self.x_tries]
    
    #bot for easy level
    def bot_handler1(self):
        self.choice = self.available_spots()
        #only makes a move for bot, which is O player
        if self.interaction % 2 != 0:
            self.interaction += 1
            #makes a random move
            self.random_choice = random.choice(self.choice)
            self.o_tries.append(self.random_choice)
            self.winner_checker()
            return 'O', self.x_y_axis[self.random_choice][0], self.x_y_axis[self.random_choice][2]
        return None, None, None
    
    #bot for medium level
    #using heuristic priority rules
    def bot_handler2(self):
        self.interaction += 1
        available = self.available_spots()
        #1. win if possible
        move = self.winning_move("O")
        if move is not None:
            self.o_tries.append(move)
            self.winner_checker()
            return "O", self.x_y_axis[move][0], self.x_y_axis[move][2]
        #2. block if other player is about to win
        move = self.winning_move("X")
        if move is not None:
            self.o_tries.append(move)
            self.winner_checker()
            return "O", self.x_y_axis[move][0], self.x_y_axis[move][2]
        #3. take center if possible
        if 4 in available:
            self.o_tries.append(4)
            self.winner_checker()
            return "O", self.x_y_axis[4][0], self.x_y_axis[4][2]
        #4. take corner if possible
        corners = [0,2,6,8]
        free_corners = [c for c in corners if c in available]
        if free_corners:
            move = random.choice(free_corners)
            self.o_tries.append(move)
            self.winner_checker()
            return "O", self.x_y_axis[move][0], self.x_y_axis[move][2]
        #5. make a random move if nothing else is possible
        move = random.choice(available)
        self.o_tries.append(move)
        self.winner_checker()
        return "O", self.x_y_axis[move][0], self.x_y_axis[move][2]

    #checks all the possible scenarios and chooses the best one after every move
    #the logic was taken from minimax algorithm examples for this game
    def minimax(self, x_tries, o_tries, is_bot_turn, depth):
        #the smaller depth, the bigger the score will be
        # and means faster the win can happen
        if self.win_combo(o_tries):
            return 10 - depth
        #the smaller depth, the faster slow will happen
        if self.win_combo(x_tries):
            return depth - 10
        #if tie, then 0
        if len(x_tries) + len(o_tries) == 9:
            return 0

        #available in given parameters
        available = [i for i in range(9) if i not in x_tries and i not in o_tries]
        #checks if the turn is the bot's and checks
        # the best possible option from the current situation
        if is_bot_turn:
            best_score = -float("inf")
            for spot in available:
                score = self.minimax(
                    x_tries,
                    o_tries + [spot],
                    False, depth + 1
                )
                best_score = max(best_score, score)
            return best_score
        #else does the same but for the opponent
        else:
            best_score = float("inf")
            for spot in available:
                score = self.minimax(
                    x_tries + [spot],
                    o_tries,
                    True, depth + 1
                )
                best_score = min(best_score, score)
            return best_score
    
    #bot for hard level
    # uses minimax algorithm    
    def bot_handler3(self):
        best_score = -float("inf")
        move = None
        self.interaction += 1

        available = self.available_spots()

    #checks every available spot and takes the biggest score spot 
        for spot in available:
            score = self.minimax(
                self.x_tries,
                self.o_tries + [spot],
                False, 0
            )

            if score > best_score:
                best_score = score
                move = spot
    #adds the cell to the taken by O list and checks if its won
        self.o_tries.append(move)
        self.winner_checker()

        return "O", self.x_y_axis[move][0], self.x_y_axis[move][2]
    #checks if there is a possible move to win the game
    def winning_move(self, player):
        available = self.available_spots()

        for spot in available:
            if player == "O":
                test = self.o_tries + [spot]
            else:
                test = self.x_tries + [spot]

            if self.win_combo(test):
                return spot
        return None
    
    #checks if the combination to win is in the list of user/bot moves
    def win_combo(self, tries):
        for combo in self.winning_combos:
            if all(pos in tries for pos in combo):
                return True
        return False
    #checks if the user/bot won and turns game_on boolean to false
    def winner_checker(self):
        if self.win_combo(self.o_tries) or self.win_combo(self.x_tries):
            self.game_on = False
        #checks if all the cells are taken and no one won, to make it draw
        elif len(self.o_tries) + len(self.x_tries) == 9:
            self.game_on = False
            self.draw = True
