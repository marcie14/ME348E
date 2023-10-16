#!/usr/bin/env python3
import serial
import time
import numpy as np

from sendStringScript import sendString
leftMotor=int(100)
rightMotor=int(100)

oldt = 0
newt = time.time() # time in s from UTC universal computer time

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

port = '/dev/ttyACM0'
String2Send = ''

def turnRight(initLeftEnc, initRightEnc):
    leftEncDiff = 0
    rightEncDiff = 0
    turn = True

    while turn == True:
        line = ser.readline().decode('utf-8')
        line = line.split(',')
        print(line)

        sendString(port,115200,'<250, -250>',0.0001) #turn right motor command here

        if(len(line) == 3):
            line = [x.replace("\r\n","") for x in line]
            leftEncDiff = float(line[0]) - initLeftEnc
            rightEncDiff = float(line[1]) - initRightEnc
            time.sleep(0.3)
        print(leftEncDiff)
        print(rightEncDiff)

        if(leftEncDiff <= -90 and rightEncDiff <= -90):
            turn = False
 
    print('it works?')

def turnLeft(initLeftEnc, initRightEnc):
    leftEncDiff = 0
    rightEncDiff = 0
    turn = True

    while turn == True:
        line = ser.readline().decode('utf-8')
        line=line.split(',')

        sendString(port,115200,'<250, -250>',0.0001) #turn right motor command here

        if(len(line) == 2):
            line = [x.replace("\r\n","") for x in line]
            leftEncDiff = float(line[0]) - initLeftEnc
            rightEncDiff = float(line[1]) - initRightEnc
        time.sleep(0.3)
        print(leftEncDiff)
        print(rightEncDiff)
        
        if(leftEncDiff >= 90 and rightEncDiff >= 90):
            turn = False
 
    print('it works?')

# line = ser.readline().decode('utf-8')
#                 #print(line)
# line=line.split(',')
# print(line)
# turnRight(line[0],line[1])   

if __name__ == '__main__':
    ser=serial.Serial(port,115200)
    #every time the serial port is opened, the arduino program will restart, very convient!
    ser.reset_input_buffer()
    ser.reset_output_buffer() #we clear the input and output buffer at the beginning of running any program to make sure
                             #that any bits left over in the buffer dont show up
    ready = 0
    

    while True:
        ser.write(String2Send.encode('utf-8'))
        #think of the below line as the default condition where no pairs of sensors are triggered as state 0, where the robot moves forward
        sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
        #ser.write(b'<'+bytes(str(leftMotor),'utf-8')+b','+bytes(str(rightMotor),'utf-8')+b'>')


        #why so I append '<' and '>' to the beginning and end of my message that I send to the arduino?

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8')
                #ive just called 2 methods from the ser object, what do they do? read the documentation and find out!
            print(line)
            line=line.split(',')
        

            # if(line[0] != "" and line[1] != ""):
            #     line = [x.replace("\r\n","") for x in line]
            #     turnRight(float(line[0]),float(line[1]))
            # time.sleep(0.3)
            # print('oops')
                #this one i wont ask you about this one is pretty self explanitory

            try:
                l=1
                # FR=int(line[0])
                # R=int(line[1])
                # MR=int(line[2])

                # ML=int(line[3])  
                # L=int(line[4])
                # FL=int(line[5])

                # BUMPS = [FL, L, ML, MR, R, FR]
                # print(BUMPS) 
                # print(newt - oldt)
            except:
                a=1
                # print("packetLost") 
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

        interval = 0.5
        count = 1
        if (newt - oldt >= interval):
            oldt = newt
            if BUMPS == [0,0,0,0,0,0]:
                print('STOP - why all pressed?')
                String2Send='<0,0>' # go stop / backwards
                sendString(port,115200,String2Send,0.0005)

            elif (BUMPS == [1,1,0,0,1,1]) or (BUMPS == [1,0,0,0,0,1]) or (BUMPS == [0,0,1,1,0,0]) or (BUMPS == [0,1,1,1,1,0]):
                print('head on collision')
                # reassign old time and new time
                String2Send='<150,-150>'#go backwards
                sendString(port,115200,String2Send,0.0005)
                
            elif 0 in BUMPS[0:3]:
            # elif (BUMPS == [0,1,1,1,1,1]) or (BUMPS == [1,0,1,1,1,1]) or (BUMPS == [0,0,1,1,1,1]) or (BUMPS == [0,0,0,1,1,1]):
                print('left collision')
                String2Send='<-150,-150>'
                sendString(port,115200,String2Send,0.0005)
            

            elif 0 in BUMPS[3:6]:
            # elif (BUMPS == [1,1,1,1,1,0]) or (BUMPS == [1,1,1,1,0,0]) or (BUMPS == [1,1,1,0,0,0]):
                print('right collsion')
                String2Send='<150,150>'
                sendString(port,115200,String2Send,0.0005)

            else:
                # print('keep driving')
                String2Send='<-200,200>'
                sendString(port,115200,String2Send,0.0005)

        # reassign old time and new time
        newt = time.time()

        # #rudimentery state machine
        # if c < 1 and x < 1: ## if either far left/right pressed
        #     sendString(port,115200,'<'+str(-leftMotor)+','+str(-rightMotor)+'>',0.0005)
        #     time.sleep(2)
        #     sendString(port,115200,'<'+str(-leftMotor)+','+str(rightMotor)+'>',0.0005)
        #     time.sleep(.5)
        #     sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)
        #     x=1
        #     y=1
        #     ########################## make unblocked
        #         # when time == ..
        # if a < 1 and z < 1: ## if either middle left/right pressed
        #    #your code here
        #    z=1
        #    a=1
        # if b < 1 and y < 1: ## if either left/right pressed
        #     #your code here
        #     b=1
        #     c=1



