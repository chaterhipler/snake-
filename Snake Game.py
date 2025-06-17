import tkinter
import random
from tkinter import Tk

ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLUMNS
WINDOW_HEIGHT = TILE_SIZE * ROWS

#game window
window = tkinter.Tk()
window.title("S-kibidi-Nake")
window.resizable(False, False)
                                                    #border width reduces the actual width to 0, highlight thickness only hides the border visually
canvas = tkinter.Canvas(window, background="black", width= WINDOW_WIDTH, height= WINDOW_HEIGHT, borderwidth= 0, highlightthickness= 0)
canvas.pack()
window.update()


#centre the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = window.winfo_width()
window_height = window.winfo_height()

window_x = int(screen_width/2 - window_width/2)
window_y = int(screen_height/2 - window_height/2)
#format (width)x(height)+(x)+(y)
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}") #don't add spaces in between the curved brackets

#initialise the game
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
def random_exclude(pStart, pEnd, exclude):
    num = random.randint(pStart, pEnd)
    while num == exclude:
        num = random.randint(pStart, pEnd)
    return num

#gloal variables
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)  #pass in the inital coordinate of the snake head
food1 = Tile(random.randint(0, COLUMNS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
food2 = Tile(random_exclude(0, COLUMNS-1, food1.x) * TILE_SIZE, random_exclude(0, ROWS-1, food1.y) * TILE_SIZE)
snake_body = [] #in tiles, excluding snake head, gets appended whenever the snake touches a food1 tile
velocityX = 0
velocityY = 0
game_over = False
score = 0
top_record = 0


def change_direction(e):   # e parameter = event, keysym = key symbol,
    #print(e)
    global velocityX, velocityY, game_over, score, food1, snake, snake_body  #dreadfully important

    if game_over:
        return

    if (e.keysym == "Up" and velocityY != 1):       #Can be looked up by print(e.keysym)
        velocityX = 0
        velocityY = -1
    elif(e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    global snake, food1, snake_body, game_over, score, top_record

    if game_over:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    #collision between snake and food
    if (snake.x == food1.x and snake.y == food1.y):
        snake_body.append(Tile(food1.x, food1.y))  #new body/head appended at the back of the array
        food1.x = random_exclude(0, COLUMNS - 1, food1.x) * TILE_SIZE
        food1.y = random_exclude(0, ROWS - 1, food1.y) * TILE_SIZE
        score += 1
    elif (snake.x == food2.x and snake.y == food2.y):
        snake_body.append(Tile(food2.x, food2.y))
        food2.x = random_exclude(0, COLUMNS-1, food1.x) * TILE_SIZE
        food2.y = random_exclude(0, ROWS -1, food1.y) * TILE_SIZE
        score += 1

    if score >= top_record:
        top_record = score

    for index in range(len(snake_body)-1, -1, -1): # from the (unfixed) length of the array -1, cuz 0 was inclusive, to -1 (cuz the last one doesn't count, so technically 0) -1 step per time
        tile = snake_body[index]   # tile = the entire 1 diemnsional subarray in the snake_body array
        if index == 0:    #the tile right before snake's head
            tile.x = snake.x
            tile.y = snake.y
        else:
            previous_tile = snake_body[index - 1]
            tile.x = previous_tile.x
            tile.y = previous_tile.y


    snake.x += velocityX * TILE_SIZE  # x an  d y are defined by user's key input
    snake.y += velocityY * TILE_SIZE  # integers are representing PIXELS instead of TILES

def reset(k):
    global snake_body, game_over, score, snake, food1, food2, velocityY, velocityX
    if k.keysym == "space":
        snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
        food1 = Tile(random.randint(0, COLUMNS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
        food2 = Tile(random_exclude(0, COLUMNS-1, food1.x) * TILE_SIZE, random_exclude(0, ROWS-1, food1.y) * TILE_SIZE)
        velocityX = 0
        velocityY = 0
        snake_body = []
        game_over = False
        score = 0

        window.bind("<KeyRelease>", change_direction)
        move()

def draw():
    global snake, food1, score

    move()
    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food1.x , food1.y, food1.x + TILE_SIZE, food1.y + TILE_SIZE, fill = "khaki")
    canvas.create_rectangle(food2.x, food2.y, food2.x + TILE_SIZE, food2.y + TILE_SIZE, fill="khaki")
    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x+TILE_SIZE, snake.y+TILE_SIZE, fill = "royal blue")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "royal blue")

    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 25", text= f"    Game Over\n\n  Top Record: {top_record}\n\nCurrent Score: {score}", fill = "white")
        window.bind("<KeyRelease>", reset)
    else:
        canvas.create_text(2 * TILE_SIZE, 1 * TILE_SIZE, font="Arial 12 ", text=f"SCORE: {score}", fill="white")

    window.after(100, draw)  #draw a frame every 100ms = 0.1 second




draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()