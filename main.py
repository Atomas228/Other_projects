from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

screen = Screen()
screen.colormode(255)
screen.setup(width=610, height=610)
screen.bgcolor(30,30,45)
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

#boolean to continue loops
game_on = True

#create a new snake and reset scoreboard
def reset():
    global game_on
    for seg in snake.segments:
        seg.hideturtle()
    snake.segments.clear()
    snake.create_snake()
    snake.head = snake.segments[0]
    scoreboard.clear()
    scoreboard.reset()
    game_on = True

#infinite while loop to make the game responsive 
# even when game is over to restart
while True:
    screen.update()
    time.sleep(0.1)
    if game_on:
        snake.move()
        screen.onkey(None, "space")
    #if the snakes head is lest than 17 px, then 'eat' it
    if snake.head.distance(food) < 17:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()        
    #if the snake collides with the wall then game over
    if snake.head.xcor() >285 or snake.head.xcor() < -285 or snake.head.ycor() > 285 or snake.head.ycor() < -285:
        game_on = False
        scoreboard.game_over()
        screen.onkey(reset, "space")

    #if the snakes head collides with it's tail, then its game over
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_on = False
            scoreboard.game_over()
            screen.onkey(reset, "space")