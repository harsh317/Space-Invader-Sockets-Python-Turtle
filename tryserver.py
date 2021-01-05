import turtle
import os
import threading
import socket
import random
import math
import winsound



sc = turtle.Screen()
sc.bgcolor("black")
sc.title("Server ")
sc.bgpic("topng.png")
to_move  = 0
bullet_to_move = ''
win_or_loose = ''
Winner = ''
chances = 0

turtle.register_shape('enemy.gif')
turtle.register_shape('asteroids.gif')

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50000))
s.listen(1)
conn, addr = s.accept()
print('connected')

connection_established = True


def receive_data(): 
    global to_move,bullet_to_move,win_or_loose,Winner,chances
    while True:
        data = conn.recv(1024).decode()
        if data == 'Loose':
            win_or_loose = 'Loose'
        elif data[:7] == 'chances':
            chances = data
            
            chances = int(''.join(filter(lambda i: i.isdigit(), chances)))        
        elif data == 'Win':
            Winner = 'Win'    
        elif data == 'bullet':
           bullet_to_move = 'bullet'        
           
        else:   
            
            to_move = int(data)
            if data:
                print(data)
    
             
     

start_thread(receive_data)

bullet = turtle.Turtle()
bullet.hideturtle()
bullet.color("yellow")
bullet.shape('triangle')
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bulletspeed = 20           
  
enemyspeed = 15  
enemy = turtle.Turtle()
enemy.color("red")
enemy.shape('enemy.gif')
enemy.penup()
enemy.speed(3)
enemy.setposition(-200,random.randint(210,250))    




def move_left():
    x = enemy.xcor()
    x -= enemyspeed
    if x < -280:
        x = -280
    conn.send(str(x).encode())    
    enemy.setx(x)
def move_right():
    x = enemy.xcor()
    x += enemyspeed
    if x > 280:
        x = 280
    conn.send(str(x).encode())    
    enemy.setx(x)    
def move_Up():       
    y = enemy.ycor()
    y += enemyspeed
    if y > 285:
        y = 285
    to_be_send = 'enemy  ',str(y) 
    to_be_send =  ''.join(to_be_send)   
    conn.send(to_be_send.encode())    
    enemy.sety(y)
def move_Down():
    y = enemy.ycor()
    y -= enemyspeed
    if y < -250:
        y = -250
        
    to_be_send = 'enemy  ',str(y) 
    to_be_send =  ''.join(to_be_send)   
    conn.send(to_be_send.encode())    
    enemy.sety(y)

    
  

turtle.listen()  
turtle.onkey(move_left,"Left")
turtle.onkey(move_right,"Right") 
turtle.onkey(move_Up,"Up") 
turtle.onkey(move_Down,"Down") 
   
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.setposition(-300,300)
pen.pendown()
pen.pensize(3)
for i in range(4):
    pen.fd(600) 
    pen.lt(-90)
    
print('chances are:',chances)    
scores = turtle.Turtle()
scores.speed(0)
scores.color('white')
scores.penup()
scores.setposition(-290,-280)
scores.write("Chances:10",False,align='left',font=("Arial",14,"normal"))    
    
image = "rocket.gif"    
sc.addshape(image)
turtle.shape(image)
turtle.penup()
turtle.setposition(0,-250)  

def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 30:
        return True
    else:
        return False


    
   
while True:
    
    if chances:
        scoremarks = "Chances:{}".format(chances)
        scores.clear()
        scores.write(scoremarks,False,align='left',font=("Arial",14,"normal"))
        chances = 0   
    
     
    turtle.setx(to_move)
    bullet.setposition(to_move,-250)
    
    if bullet_to_move:
         winsound.PlaySound('bullet.wav',winsound.SND_ASYNC)
         while True:
            y = bullet.ycor()
            y += bulletspeed
            bullet.sety(y)
            bullet.showturtle()
            bullet_to_move = ''
            if bullet.ycor() > 275:
                bullet.hideturtle()
                bullet_to_move = ''
                break
            
                
                
    if to_move < -280:
        to_move = -280
        turtle.setx(to_move)
    if to_move > 280:
        to_move = 280
        turtle.setx(to_move)    
    pass

    if isCollision(turtle,enemy):
        winsound.PlaySound('winning.wav',winsound.SND_ASYNC)
        conn.send('Loose'.encode())
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Won", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('You Won')
        break
    
    if win_or_loose == 'Loose':
        winsound.PlaySound('loosing.wav',winsound.SND_ASYNC)
        print('looser')
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Loose", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
        break
    
    if Winner == 'Win':
        scores.clear()
        scores.write('Chances:0',False,align='left',font=("Arial",14,"normal"))
        winsound.PlaySound('winning.wav',winsound.SND_ASYNC)
        print('Winner')
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Won", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
        break   



            
            
delay = input('Press Enter to finish' )
