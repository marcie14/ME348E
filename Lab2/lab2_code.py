#!/usr/bin/env python3
import serial
import time
import numpy as np

from sendStringScript import sendString
leftMotor=int(100)
rightMotor=int(100)

t = time

FR=int(1)
R=int(1)
MR=int(1) #a bump sensor that is unactivated starts at 1 (because they are pullups), hence why these are all one
ML=int(1)
L=int(1)
FL=int(1)

x = FR
y = R
z = MR
a = ML
b = L
c = FL
BUMPS = [1,1,1,1,1,1]

if __name__ == '__main__':
    ser=serial.Serial('/dev/ttyACM0',115200)
    #every time the serial port is opened, the arduino program will restart, very convient!
    ser.reset_input_buffer()
    ready = 0
    

    while True:
        
        #think of the below line as the default condition where no pairs of sensors are triggered as state 0, where the robot moves forward
        sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
        #ser.write(b'<'+bytes(str(leftMotor),'utf-8')+b','+bytes(str(rightMotor),'utf-8')+b'>')


        #why so I append '<' and '>' to the beginning and end of my message that I send to the arduino?

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8')
                #ive just called 2 methods from the ser object, what do they do? read the documentation and find out!
            line=line.split(',')
                #this one i wont ask you about this one is pretty self explanitory

            try:
                    
                FR=int(line[0])
                R=int(line[1])
                MR=int(line[2])

                ML=int(line[3])  
                L=int(line[4])
                FL=int(line[5])

                BUMPS = [FL, L, ML, MR, R, FR]
                print(BUMPS) 
                
            except:
                print("packetLost") 
                #why do I have this exepction? 



       
            

        # match bumps:
        #     case [0,0,0,0,0,0]:
        #         print('STOP - why all pressed?')
        #     case [0,1,1,1,1,1]:
        #         print('left collision')
        #     case [0,0,1,1,1,1]:
        #         print('left collision')
        #     case [0,0,0,1,1,1]:
        #         print('left collision')
        #     case [1,1,0,0,1,1]:
        #         print('head on collision')
        #     case [1,1,1,1,1,0] | [1,1,1,1,0,0] | [1,1,1,0,0,0]:
        #         print('right collision')
        #     case other:
        #         print('keep driving')

        if BUMPS == [0,0,0,0,0,0]:
            print('STOP - why all pressed?')
        elif (BUMPS == [0,1,1,1,1,1]) or (BUMPS == [0,0,1,1,1,1]) or (BUMPS == [0,0,0,1,1,1]):
            print('left collision')
            sendString('/dev/ttyACM0',115200,'<'+str(-leftMotor)+','+str(-rightMotor)+'>',0.0005)
            time.sleep(2)
            sendString('/dev/ttyACM0',115200,'<'+str(-leftMotor)+','+str(rightMotor)+'>',0.0005)
            time.sleep(.5)
            sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
            x=1
            y=1
        elif (BUMPS == [1,1,1,1,1,0]) or (BUMPS == [1,1,1,1,0,0]) or (BUMPS == [1,1,1,0,0,0]):
            print('right collsion')
        elif (BUMPS == [1,1,0,0,1,1]) or (BUMPS == [1,0,0,0,0,1]):
            print('head on collision')
        else:
            print('keep driving')

        #rudimentery state machine
        if c < 1 and x < 1: ## if either far left/right pressed
            sendString('/dev/ttyACM0',115200,'<'+str(-leftMotor)+','+str(-rightMotor)+'>',0.0005)
            time.sleep(2)
            sendString('/dev/ttyACM0',115200,'<'+str(-leftMotor)+','+str(rightMotor)+'>',0.0005)
            time.sleep(.5)
            sendString('/dev/ttyACM0',115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
            x=1
            y=1
            ########################## make unblocked
                # when time == ..
        if a < 1 and z < 1: ## if either middle left/right pressed
           #your code here
           z=1
           a=1
        if b < 1 and y < 1: ## if either left/right pressed
            #your code here
            b=1
            c=1


