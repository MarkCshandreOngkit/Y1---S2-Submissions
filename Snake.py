#Program Name: Snake
#Creator: Mark Cshandre C. Ongkit
#Date: February 28, 2025

from tkinter import *
import random

#Constances
GAME_WIDTH = 900
GAME_HEIGHT = 900
TILE_SIZE = 30
SPEED = 100
BODY_PARTS = 2
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000" 
BACKGROUND = "#000000"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([(5 * TILE_SIZE), (5 * TILE_SIZE)])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)
class Food:
    
    def __init__(self):

        x = random.randint(0, int(GAME_WIDTH / TILE_SIZE) - 1) * TILE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / TILE_SIZE) - 1) * TILE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + TILE_SIZE, y + TILE_SIZE, fill = FOOD_COLOR, tag = "food")
        

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= TILE_SIZE
    elif direction == "down":
        y += TILE_SIZE
    elif direction == "left":
        x -= TILE_SIZE
    elif direction == "right":
        x += TILE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill = SNAKE_COLOR, tag = "snake")

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        #food collision scoring
        global score
        score += 1

        label.config(text = "Score: {}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()

    else:
        windows.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

def retry(try_again):
    global direction, score

    if try_again:
        score = 0
        label.config(text = "Score: {}".format(score))
        canvas.delete(ALL)
        direction = "down"
        snake = Snake()
        food = Food()

        next_turn(snake, food)



def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, text = "GAME OVER", font = ("Arial, 90"), fill = "red", tag = "gameover")
    canvas.create_text((canvas.winfo_width() / 2), (canvas.winfo_height() / 2) + 75, text = "(Press 'Spacebar' to try again)", font = ("Arial, 15"), fill = "white", tag = "gameover")
    windows.bind('<space>',lambda event: retry(True))



#game window
windows = Tk()
windows.title("Snake")
windows.resizable(False, False)

#score
score = 0
label = Label(windows, text = "Score: {}".format(score), font = "Arial, 30")
label.pack()

canvas = Canvas(windows, bg = BACKGROUND, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

windows.update()

#producing game window in center
windows_width = windows.winfo_width()
windows_height = windows.winfo_height()
screen_width = windows.winfo_screenwidth()
screen_height = windows.winfo_screenheight()

x = int((screen_width / 2) - (windows_width / 2))
y = int((screen_height / 2) - (windows_height / 2)) - 25

windows.geometry(f"{windows_width}x{windows_height}+{x}+{y}")

#movement
windows.bind('<Left>' and '<a>', lambda event: change_direction('left'))
windows.bind('<Right>' and '<d>', lambda event: change_direction('right'))
windows.bind('<Up>' and '<w>', lambda event: change_direction('up'))
windows.bind('<Down>' and '<s>', lambda event: change_direction('down'))

#intialize game

direction = "down"
snake = Snake()
food = Food()

next_turn(snake, food)

windows.mainloop()

#problem: if you presed a, s, d or left, down, right fast enough, you can do 180 turns