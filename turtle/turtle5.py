#!/usr/bin/python3
from turtle import *
import numpy as np
import time

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
  if (x1 - x) ** 2 + (y1 - y) ** 2 >= 20 ** 2:
    alpha = np.arctan2((x - x1), (y - y1))
    dx = np.sin(alpha)
    dy = np.cos(alpha)
    x1 = x if x >= x1 and x <= x1+dx else x1 + dx 
    y1 = y if y >= y1 and y <= y1+dy else y1 + dy
    t1.goto(x1, y1)
  else:
    t1.goto(x1, y1)
  #t1.clear()
  

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
