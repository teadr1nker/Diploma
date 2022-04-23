#!/usr/bin/python3
from turtle import *
 
v = 0 #максимальная скорость черепашки
step = 1
wn = Screen()
t = Turtle()
t.color('blue')
t.width(5)
t.shape('circle')
t.penup()
t.speed(v)

t1 = Turtle()
t1.color('red')
t1.width(5)
t1.shape('circle')
t1.penup()
t1.speed(1)
t1.goto(100, 100)
 
def draw(x, y):
  t.goto(x, y)
  
 
def move(x, y):
  t.goto(x, y)
 
def stepUp():
 t.goto(t.xcor(), t.ycor() + step)
 
def stepDown():
 t.goto(t.xcor(), t.ycor() - step)
 
def stepLeft():
 t.goto(t.xcor() - step, t.ycor())
 
def stepRight():
 t.goto(t.xcor() + step, t.ycor())

t.ondrag(draw)
 
scr = t.getscreen()
scr.onscreenclick(move)
scr.onkey(stepUp,'Up')
scr.onkey(stepDown,'Down')
scr.onkey(stepLeft,'Left')
scr.onkey(stepRight,'Right')
 
scr.listen()

while 1:
  x, y = (t.xcor(), t.ycor())
  t1.goto(x, y)
	
wn.mainloop()                    
