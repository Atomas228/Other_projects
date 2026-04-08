from turtle import Screen
from boardpart import Board
from osnxs import Osandxs
from scoreboard import Scoreboard
from choose_game import Choose_game
from game_logic import Game_logic
screen = Screen()
screen.setup(600,600)
screen.colormode(255)
screen.title("Tic Tac Toe Game")
screen.bgcolor(174, 214, 207)
screen.tracer(0)
interaction = 0
osandxs = Osandxs()
board = Board()
scoreboard = Scoreboard()
choose_game = Choose_game()
game_logic = Game_logic()
#boolean in a list to not make global boolean variables
bot_playing = [False]   
#pops up the question about PvP or bot
choose_game.first_question()

#handles the first question click(1-bot, 2-PvP)
def click_handler(x,y):
    choose_game.choose_player(x,y)
    if choose_game.player == 2:
        reset()
        board.create_board()
        choose_game.clear()
    elif choose_game.player == 1:
        choose_game.clear()
        choose_game.second_question()
        screen.onclick(level_handler)
        
#handles the level question
def level_handler(x, y):
    choose_game.choose_level(x,y)
    choose_game.clear()
    board.create_board()
    bot_playing[0] = True
    reset() 

#resets the game
def reset():
    game_logic.reset()
    osandxs.mark.clear()
    scoreboard.clear()
    scoreboard.reset()
    screen.onkey(None, "space") 
    #if bot is playing then handles the bot v player logic
    if bot_playing[0] == True:
        screen.onclick(botv1)
    else:
        screen.onclick(move_handler)


def botv1(x,y):
    #if game is not on or you cant click in the moment, then returns nothing
    if not game_logic.game_on or game_logic.input_locked:
        return
    #but then else if possible then let the user click and lock right away 
    # and let the if statements handle the move and then make a bot move after half a second
    game_logic.input_locked = True
    move_handler(x,y)
    if not game_logic.game_on:
        return
    screen.ontimer(bot_move, 500)


def move_handler(x,y):
    #if its a bot and its bot's move then based on the level, make bot move
    if bot_playing[0] == True and game_logic.interaction % 2 != 0:
        if choose_game.game_level == 1:
            player_mark, x_axis, y_axis = game_logic.bot_handler1()
        elif choose_game.game_level == 2:
            player_mark, x_axis, y_axis = game_logic.bot_handler2()
        elif choose_game.game_level == 3:
            player_mark, x_axis, y_axis = game_logic.bot_handler3()
    else:
    #else make the person move
        player_mark, x_axis, y_axis = game_logic.move_handler(x,y)
    #if nothing is returned from game logic then dont make anything
    if player_mark == None:
        return
    #draw a mark based on a player
    if player_mark == "X":
        osandxs.draw_xs(x_axis,y_axis)
    elif player_mark == "O":
        osandxs.draw_os(x_axis,y_axis)
    #check the winner
    winner_handler()

def bot_move():
    move_handler(None,None)
    game_logic.input_locked = False

def winner_handler():
    #check if someone won
    if game_logic.win_combo(game_logic.x_tries):
        scoreboard.increase_score("X")
        scoreboard.game_over("X")
        screen.onclick(None)
        screen.onkey(reset, "space")
    elif game_logic.win_combo(game_logic.o_tries):
        scoreboard.increase_score("O")
        scoreboard.game_over("O")
        screen.onclick(None)
        screen.onkey(reset, "space")
    #or drew
    elif game_logic.draw:
        scoreboard.game_over("tie")
        screen.onkey(reset, "space")


screen.listen()
screen.onclick(click_handler)

screen.mainloop()