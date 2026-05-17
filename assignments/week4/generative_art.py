from turtle import *
import random

width = 400
height = 400
setup(width, height)

tracer(0, 0)

bgcolor('white')

colors = ['red', 'green', 'blue', 'yellow']
face_color = random.choice(colors)

if face_color == 'red':
    bgcolor('blue')
elif face_color == 'green':
    bgcolor('yellow')
elif face_color == 'yellow':
    bgcolor('green')
elif face_color == 'blue':
    bgcolor('red')


penup()
goto(0,-100)
pendown()
#face
fillcolor(random.choice(colors))
begin_fill()
circle(100, 360)
end_fill()
#eyes
for x in [-35, 30]:
    penup(); goto(x, 20); pendown()
    color('black')
    begin_fill(); circle(10); end_fill()
#smile
penup(); goto(-48, -20); pendown()
setheading(-54)
circle(50, 115)





update()
exitonclick()
