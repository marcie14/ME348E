#!/usr/bin/env python3
import serial
import time
import numpy as np
from sendStringScript import sendString
leftMotor=int(100)
rightMotor=int(100)

now = time.time()
old = 0
port = '/dev/ttyACM1'


if __name__ == '__main__':
    ser=serial.Serial(port,115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.

    while True:
        sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0001)
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
                 
                line = ser.readline().decode('utf-8')
                line=line.split(',')
                #this splits the incoming string up by commas
                try:
                    
                    x=int(line[0])
                    y=int(line[1])
                    z=int(line[2]) #we dont convert this to a float becasue we went to be able to recieve the message that we are at a cross, which wont be an int. 
                    print([x,y,z])
                    print(now)
                    print(old)
                except:
                    print("packet dropped") #this is designed to catch when python shoves bits on top of each other. 


            
            
                #Following is my control law, we're keeping it basic for now, writing good control law is your job
                #ok so high numbers(highest 7000) on the line follwing mean I am too far to the LEFT,
                #low numbers mean I am too far on the RIGHT, 3500 means I am at the middle
                #below is a basic control law you can send to your motors, with an exeption if z is a value greater than 7000, meaning the arduino code sees that the line sensor is on a cross. Feel free to take insperation from this,
            #but you will need to impliment a state machine similar to what you made in lab 2 (including a way of counting time without blocking)
                if (now - old) > .01:
                    old = now
                    now = time.time()
                    if not z < 7000: #im assuming that in your arduino code you will be setting z to the int 8000 if you sense a cross, dont feel obligated to do it this way.  
                        leftMotor=100+.02*z #now that we are SURE that z isnt the string cross, we cast z to an int and recalculate leftMotor and rightMotor, 
                        rightMotor=250-.02*z
                    elif z < 3500:
                        leftMotor = 0 ### need to fix - marcie
                        rightMotor = 0 ### need to fix - marcie
                        print('DETECT LEFT, MOVING RIGHT')
                    elif z == 3500:
                        leftMotor = 0 ### need to fix - marcie
                        rightMotor = 0 ### need to fix - marcie
                        print('DETECT CENTER - STRAIGHT')
                    elif z > 3500:
                        leftMotor = 0 ### need to fix - marcie
                        rightMotor = 0 ### need to fix - marcie
                        print('DETECT RIGHT, MOVING LEFT')
                    else:
                        print('at intersection')
                        #do something here like incrimenting a value you call 'lines_hit' to one higher, and writing code to make sure that some time (1 second should do it) 
                        # passes between being able to incriment lines_hit so that it wont be incrimented a bunch of times when you hit your first cross. IE give your robot time to leave a cross
                        #before allowing lines_hit to be incrimented again.
