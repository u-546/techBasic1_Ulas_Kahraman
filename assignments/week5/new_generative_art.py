"""This code draws smiley faces in various colors using turtle
This is the refactored version from a previous version with constants defined and a function for picking colors added.
function and define does make this color picking mechanic easier to read.
Besides looking at the week5 files, I've consulted Claude ai on ways to make code more understandable and looked for some examples on youtube.
https://www.youtube.com/watch?v=rp1QR3eGI1khttps://www.youtube.com/watch?v=rp1QR3eGI1k
this video was also helpful in understanding the basic idea behind refactoring codes."""


from turtle import *
import random

#Constants
WIDTH = 400
HEIGHT = 400
COLORS = ['red', 'green', 'blue', 'yellow']

# Each face color gets assigned a contrasting background color
CONTRAST = {
    'red':    'blue',
    'blue':   'red',
    'green':  'yellow',
    'yellow': 'green',
}


#Function
def pick_colors(colors):
    """Pick a random face color and return its matching background color.

    How it works:
        1. random.choice(colors) picks one color from the list.
        2. contrasting colors: red gives us blue
        3. Both values are returned together as a pair

    """
    face_color = random.choice(colors)
    bg_color = CONTRAST[face_color]
    return face_color, bg_color


#Main
def main():
    # Set up the window
    setup(WIDTH, HEIGHT)
    tracer(0, 0)

    # Use the function to get both colors at once
    face_color, bg_color = pick_colors(COLORS)
    bgcolor(bg_color)

    # Draw the face
    penup()
    goto(0, -100)
    pendown()
    fillcolor(face_color)
    begin_fill()
    circle(100, 360)
    end_fill()

    # Draw the eyes
    for x in [-35, 30]:
        penup(); goto(x, 20); pendown()
        color('black')
        begin_fill(); circle(10); end_fill()

    # Draw the smile
    penup(); goto(-48, -20); pendown()
    setheading(-54)
    circle(50, 115)

    update()
    exitonclick()


# Run the program
main()
