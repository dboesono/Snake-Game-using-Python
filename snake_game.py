import turtle
import time
import random

# Starting Variables
time = 0
stamp_x_coordinates = []
stamp_y_coordinates = []
contact = 0
tail_length = 5
current_tail= 0
food = turtle.Turtle()
food.hideturtle()
food.penup()
food.speed(0)
food_numbers = []
food_numbers_x_cor = []
food_numbers_y_cor = []
food_status = []
# Movement starting variables
collision = False
first_move = True
pause_status = True
g_direction = 'Paused'

# Set up the screen.
wn = turtle.Screen()
wn.title("Snake Game By Darren Boesono_120040022")
wn.bgcolor("white")
wn.setup(width = 740, height = 660)
wn.tracer(0) #Turns off the screen update

game_area = turtle.Turtle("square")
game_area.hideturtle()
game_area.penup()
game_area.speed(0)
game_area.goto(-250,210)
game_area.pendown()
game_area.forward(500)
for i in range(3):
    game_area.right(90)
    game_area.forward(500)

status_area = turtle.Turtle("square")
status_area.hideturtle()
status_area.penup()
status_area.speed(0)
status_area.goto(250, 210)
status_area.pendown()
status_area.left(90)
status_area.forward(80)
status_area.left(90)
status_area.forward(500)
status_area.left(90)
status_area.forward(80)

wn.update()

motion_status = turtle.Turtle('square')
motion_status.hideturtle()
motion_status.penup()
motion_status.speed(0)
motion_status.goto(30,240)

contact_turtle = turtle.Turtle('square')
contact_turtle.hideturtle()
contact_turtle.penup()
contact_turtle.speed(0)
contact_turtle.goto(-200,240)

timer_turtle = turtle.Turtle('square')
timer_turtle.hideturtle()
timer_turtle.penup()
timer_turtle.speed(0)
timer_turtle.goto(-80, 240)

# Creating the snake
head = turtle.Turtle('square')
head.penup()

# Creating the monster
monster = turtle.Turtle('square')
monster.color('black', 'purple')
monster.penup()


# Movement Functions
def go_up():
    head.direction = "up"

def go_down():
    head.direction = "down"

def go_left():
    head.direction = "left"

def go_right():
    head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Keyboard bindings
def keyboard():
    wn.listen()
    wn.onkeypress(go_up, "Up")
    wn.onkeypress(go_down, "Down")
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")


# The starting position
def StartingPosition():
    global snake_x_cor
    global snake_y_cor

    snake_x_cor = 20 * random.randint(-12, 12)
    snake_y_cor = 20 * random.randint(-14,10)
    head.goto(snake_x_cor, snake_y_cor)
    while True:
        monster_x_cor = 20 * random.randint(-12, 12)
        monster_y_cor = random.randint(-14, 10)
        monster.goto(monster_x_cor, monster_y_cor)
        if head.distance(monster) > 100:
            break


# The movement of the monster
def MonsterMove():
    if first_move == False:
        if abs(head.xcor() - monster.xcor()) > abs(head.ycor() - monster.ycor()):
            if head.xcor() > monster.xcor():
                monster.setheading(0)
            else:
                monster.setheading(180)

        else:
            if head.ycor() > monster.ycor():
                monster.setheading(90)
            else:
                monster.setheading(270)
        monster.forward(20)

    for i in range(len(stamp_x_coordinates)):
        if abs(monster.xcor() - stamp_x_coordinates[i]) < 20:
            if abs(monster.ycor() - stamp_y_coordinates[i]) < 20:
                updateContact()
                break


    wn.update()
    if (gameOver() == False):
        wn.ontimer(MonsterMove, 1000)
    else:
        if (result == 'w'):
            head.color('blue')
            head.write('YOU WIN')
            head.color('black')
        else:
            head.color('red')
            head.write('YOU LOSE')
            head.color('black')


# Showing the motion label
def ShowMotion():
    motion = "Motion: "
    motion += g_direction
    motion_status.clear()
    motion_status.write(motion, align='Left')


# Generating the food
def GenerateFood():
    global food_numbers
    global food_numbers_x_cor
    global food_numbers_y_cor
    global food_status

    for i in range(9):
        food_numbers.append(turtle.Turtle("square"))
        while True:
            random_x_cor = random.randint(-12, 12)
            random_y_cor = random.randint(-14, 10)
            if (random_x_cor, random_y_cor) not in zip(food_numbers_x_cor, food_numbers_y_cor):
                if ((random_x_cor, random_y_cor) != (snake_x_cor / 20, snake_y_cor / 20)):
                    food_numbers_x_cor.append(random_x_cor)
                    food_numbers_y_cor.append(random_y_cor)
                    break
        food_numbers[i].hideturtle()
        food_numbers[i].speed(0)
        food_numbers[i].penup()
        food_numbers[i].goto(random_x_cor*20, random_y_cor*20 - 10)
        food_status.append(False)

# Labeling the food
def WriteFood():
    for i in range (9):
        food_numbers[i].clear()
        if food_status[i] == False:
            food_numbers[i].write(i + 1, align = 'Center')

def checkFood():
    global food_status
    global tail_length
    l_xcor = round(head.xcor(), 0)
    l_ycor = round(head.ycor(), 0)
    for i in range(9):
        if abs(l_xcor - food_numbers_x_cor[i] * 20) < 20:
            if abs(l_ycor - food_numbers_y_cor[i] * 20) < 20:
                if food_status[i] == False:
                    food_status[i] = True
                    tail_length += (i + 1)
                    break


# Pausing the game
def pause():
    global pause_status
    global g_direction
    if pause_status == True and first_move == False:
        motion = 'Motion : '
        motion += g_direction
        motion_status.clear()
        motion_status.write(motion, align='Left')
        pause_status = False
    else:
        motion_status.clear()
        motion_status.write('Motion : Paused')
        pause_status = True


def check_border_collision():
    global pause_status
    global collision

    if head.xcor() == 240 and g_direction == 'Right':
        pause_status = True
        collision = True

    if head.xcor() == -240 and g_direction == 'Left':
        pause_status = True
        collision = True

    if head.ycor() == 200 and g_direction == 'Up':
        pause_status = True
        collision = True

    if head.ycor() == -280 and g_direction == 'Down':
        pause_status = True
        collision = True


def wn_forward():
    global current_tail
    global stamp_x_coordinates
    global stamp_y_coordinates

    WriteFood()
    speed = 200
    check_border_collision()
    checkFood()

    if (gameOver()):
        return None
    if (pause_status == True):
        pass
    else:
        if current_tail < tail_length:
            speed = 260

        head.color('black', 'red')
        head.stamp()
        stamp_x_coordinates.append(round(head.xcor()))
        stamp_y_coordinates.append(round(head.ycor()))
        head.forward(20)
        head.color('black')
        current_tail += 1

        if (current_tail > tail_length):
            head.clearstamps(1)
            current_tail -= 1
            stamp_x_coordinates = stamp_x_coordinates[1:]
            stamp_y_coordinates = stamp_y_coordinates[1:]

    wn.update()
    wn.ontimer(wn_forward, speed)


def gameOver():
    global result
    if tail_length == 50:
        result = 'w'
        return True
    elif head.distance(monster) < 20:
        result = 'l'
        return True
    return False

def updateContact():
    global contact
    txt = 'Contact : '
    contact += 1
    txt += str(contact)
    contact_turtle.clear()
    contact_turtle.write(txt, align='Left')


def GoUp():
    global g_direction, pause_status
    global head
    global first_move, collision

    first_move = False

    if g_direction != 'Down':
        head.setheading(90)
        g_direction = 'Up'

    if pause_status:
        if collision == True:
            if g_direction != 'Down':
                head.setheading(90)
                g_direction = 'Up'
        else:
            head.setheading(90)
            g_direction = 'Up'

    ShowMotion()
    pause_status = False
    collision = False


def GoDown():
    global g_direction, pause_status
    global head
    global first_move, collision

    first_move = False

    if g_direction != 'Up':
        head.setheading(270)
        g_direction = 'Down'

    if pause_status:
        if collision == True:
            if g_direction != 'Up':
                head.setheading(270)
                g_direction = 'Down'
        else:
            head.setheading(270)
            g_direction = 'Down'

    pause_status = False
    collision = False
    ShowMotion()


def GoRight():
    global g_direction, pause_status
    global head
    global first_move, collision

    first_move = False

    if g_direction != 'Left':
        head.setheading(0)
        g_direction = 'Right'

    if pause_status:
        if collision == True:
            if g_direction != 'Left':
                Head.setheading(0)
                g_direction = 'Right'
        else:
            head.setheading(0)
            g_direction = 'Right'

    pause_status = False
    collision = False
    ShowMotion()


def GoLeft():
    global g_direction, pause_status
    global head
    global first_move, collision

    first_move = False

    if g_direction != 'Right':
        head.setheading(180)
        g_direction = 'Left'

    if pause_status:
        if (collision == True):
            if g_direction != 'Right':
                head.setheading(180)
                g_direction = 'Left'
        else:
            head.setheading(180)
            g_direction = 'Left'

    pause_status = False
    collision = False
    ShowMotion()


def timer():
    global time

    if gameOver():
        return None

    timer_turtle.clear()
    time += 1
    txt = 'Time : ' + str(time)
    timer_turtle.write(txt, align='Left')

    wn.update
    wn.ontimer(timer, 1000)


def initiateGame(x, y):
    intro_turtle.clear()
    motion_status.write('Motion : Paused', align='Left')
    contact_turtle.write('Contact : 0', align='Left')
    timer_turtle.write('Time : 0', align='Left')
    wn.listen()
    wn.onkey(GoUp, "Up")
    wn.onkey(GoDown, "Down")
    wn.onkey(GoLeft, "Left")
    wn.onkey(GoRight, "Right")
    wn.onkey(pause, 'space')
    wn.ontimer(timer, 1000)
    wn_forward()
    MonsterMove()

intro = "Welcome to the Darren Boesono's snake game! \nClick anywhere to start!"

intro_turtle = turtle.Turtle()
intro_turtle.hideturtle()
intro_turtle.penup()
intro_turtle.goto(-240,150)
intro_turtle.write(intro, align='Left')
StartingPosition()
GenerateFood()

wn.onclick(initiateGame)



wn.mainloop()