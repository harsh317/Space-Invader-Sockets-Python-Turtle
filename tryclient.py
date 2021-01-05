import turtle
import os
import socket
import threading
import math
import re
import winsound
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Space Invaders")

turtle.register_shape('enemy.gif')

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

HOST = 'localhost' 
PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
to_move_enemy = 0
to_move_enemy_up = 0
win_or_loose = ''
chances = 10
while not connected:
    try:
        sock.connect((HOST,PORT))
        connected = True
        screen.bgpic("topng.png")
        connection_established = True
    except:
        print("Waiting for connection....")
        pass

def receive_data():
    global to_move_enemy,to_move_enemy_up,win_or_loose
    while True:
        data = sock.recv(1024).decode()
        print('decoded is',data)
        if data == 'Loose':
            win_or_loose = 'Loose'
        elif data[:5] == 'enemy':
            to_move_enemy_up = data
            to_move_enemy_up = [int(d) for d in re.findall(r'-?\d+', to_move_enemy_up)]
            to_move_enemy_up = to_move_enemy_up[0]
        else:
            to_move_enemy = int(data)        
start_thread(receive_data)
        
#Draw border
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.setposition(-300,-300)
pen.pendown()
pen.pensize(3)
for side in range(4):
	pen.fd(600)
	pen.lt(90)
pen.hideturtle()	

scores = turtle.Turtle()
scores.speed(0)
scores.color('white')
scores.penup()
scores.setposition(-290,-280)
scoremarks = "Chances:{}".format(chances)
scores.write(scoremarks,False,align='left',font=("Arial",14,"normal"))


scores.hideturtle()

image = "rocket.gif"    
screen.addshape(image)
turtle.shape(image)
turtle.penup()
turtle.setposition(0, -250)


playerspeed = 15
enemyspeed = 3

#Create the enemy
enemy = turtle.Turtle()
enemy.color("red")
enemy.shape("enemy.gif")
enemy.penup()
enemy.speed(0)
enemy.setposition(-200, 250)



#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 25


bulletstate = "ready"


#Move the player left and right
def move_left():
    x = turtle.xcor()
    x -= playerspeed
    print(x)    
    if connection_established == True:
        sock.send(str(x).encode())
    if x < -280:
        x = - 280
    turtle.setx(x)
	
def move_right():
    x = turtle.xcor()
    x += playerspeed
    print(x)
    if connection_established == True:
        sock.send(str(x).encode())
    if x > 280:
        x = 280
    turtle.setx(x)
	
def fire_bullet():
	#Declare bulletstate as a global if it needs changed
    global bulletstate,chances
    chances -= 1
    to_send = 'chances',str(chances)
    to_send = ''.join(to_send)
    sock.send(to_send.encode())
    if chances == 0 and not isCollision(bullet,enemy):
        winsound.PlaySound('loosing.wav',winsound.SND_ASYNC)
        sock.send('Win'.encode())
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Loose", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
                
    scoremarks = "Chances:{}".format(chances)
    scores.clear()
    scores.write(scoremarks,False,align='left',font=("Arial",14,"normal"))
    if bulletstate == "ready":
        winsound.PlaySound('bullet.wav',winsound.SND_ASYNC)
        bulletstate = "fire"
		#Move the bullet to the just above the player
        x = turtle.xcor()
        y = turtle.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
  
def isCollision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 30:
        return True
    else:
        return False

#Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#Main game loop
while True:
    if to_move_enemy:
        enemy.setx(to_move_enemy)
    if to_move_enemy_up:
        enemy.sety(to_move_enemy_up)    

		
	#Move the bullet
    if bulletstate == "fire":

        y = bullet.ycor()
        y += bulletspeed
        if connection_established == True:
            to_be_send = 'bullet'             
            sock.send(to_be_send.encode())
        bullet.sety(y)
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    if isCollision(bullet,enemy) and chances == 0 :
        sock.send('Loose'.encode())
        winsound.PlaySound('winning.wav',winsound.SND_ASYNC)
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Won", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
        break

    if isCollision(bullet,enemy):
        sock.send('Loose'.encode())
        winsound.PlaySound('winning.wav',winsound.SND_ASYNC)
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Won", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
        break
    
    if win_or_loose == 'Loose':
        winsound.PlaySound('loosing.wav',winsound.SND_ASYNC)
        bullet.hideturtle()
        enemy.hideturtle()
        turtle.hideturtle()
        turtle.color('red')
        turtle.setposition(-80,0)
        turtle.write("You Loose", font=('Arial', 50, 'normal', 'bold', 'italic', 'underline'))
        print('Game Over')
        break
    
        
   


screen.mainloop()