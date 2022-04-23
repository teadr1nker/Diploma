#!/usr/bin/python3
from turtle import *
import numpy as np
 
v = 0 #максимальная скорость черепашки
step = 50
wn = Screen()  #pointer
t = Turtle()
t.color('blue')
t.width(5)
t.shape('circle')
t.penup()
t.speed(v)

t1 = Turtle()  #turtle "robot"
t1.color('red')
t1.width(5)
t1.shape('circle')
t1.penup()
t1.speed(10)
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

def stepTo(x, y):
  #delta = 2
  x1, y1 = (t1.xcor(), t1.ycor())
  alpha = np.arctan2((x - x1), (y - y1))
  #print(alpha * 180 / np.pi)
  #t1.write(f'angle: {alpha * 180 / np.pi}')
  x1 += np.sin(alpha)
  y1 += np.cos(alpha)
  t1.goto(x1, y1)
  t1.clear()

scr = t.getscreen()

scr.onscreenclick(move)
scr.onkey(stepUp,'Up')
scr.onkey(stepDown,'Down')
scr.onkey(stepLeft,'Left')
scr.onkey(stepRight,'Right')
 
scr.listen()

while 1:
  x, y = (t.xcor(), t.ycor())
  stepTo(x, y)
	
wn.mainloop()                    
