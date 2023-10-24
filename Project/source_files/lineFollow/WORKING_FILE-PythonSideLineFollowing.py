#!/usr/bin/env python3
import serial
import time
import numpy as np
from sendStringScript import sendString
leftMotor=int(100)
rightMotor=int(100)
num_intersections = 0

now = time.time()
old = 0
cross_time_old = 0
cross_time_new = time.time()
port = '/dev/ttyACM0'
String2Send = ''
LINE_turn = []
turn = False

def turnRight(initLeftEnc, initRightEnc):
    leftEncDiff = 0
    rightEncDiff = 0
    turn = True

    while turn == True:
        line = ser.readline().decode('utf-8')
        line = line.split(',')

        sendString(port,115200,'<250, -250>',0.0001) #turn right motor command here

        if(len(line) == 2):
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

if __name__ == '__main__':
    ser=serial.Serial(port,115200)
    #every time the serial port is opened, the arduino program will restart, very convient!
    ser.reset_input_buffer()
    ser.reset_output_buffer() #we clear the input and output buffer at the beginning of running any program to make sure
                             #that any bits left over in the buffer dont show up
    ready = 0
    # while True:
    #     ser.write(String2Send.encode('utf-8'))
    #     sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0005)

    #     if ser.in_waiting > 0:
    #         line = ser.readline().decode('utf-8')
    #                     #ive just called 2 methods from the ser object, what do they do? read the documentation and find out!
    #         print(line)
    #         line=line.split(',')
    #         # if(len(line) == 2 and line[0] != "" and line[1] != ""):
    #         #     line = [x.replace("\r\n","") for x in line]
    #         #     turnRight(float(line[0]),float(line[1]))
    #         # time.sleep(0.3)
                

    while True:
        sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0001)
        
        now = time.time() # constantly reassign new timestamp
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            #### remove below (debug) ####

            # leftMotor +=1
            # rightMotor +=1
            
            # if leftMotor > 400 or rightMotor > 400:
            #     break

            #sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0001)
            #### remove above (debug) ####


            line = ser.readline().decode('utf-8')
            line=line.split(',')
            print(line)
            #this splits the incoming string up by commas
            try:
                
                x = int(line[0])
                y = int(line[1])
                z = int(line[2]) #we dont convert this to a float becasue we went to be able to recieve the message that we are at a cross, which wont be an int. 
                print([x,y,z])
                # print(now)
                # print(old)
            except:
                print("packet dropped") #this is designed to catch when python shoves bits on top of each other. 

            time.sleep(0.3)
        
        
            #Following is my control law, we're keeping it basic for now, writing good control law is your job
            #ok so high numbers(highest 7000) on the line follwing mean I am too far to the LEFT,
            #low numbers mean I am too far on the RIGHT, 3500 means I am at the middle
            #below is a basic control law you can send to your motors, with an exeption if z is a value greater than 7000, meaning the arduino code sees that the line sensor is on a cross. Feel free to take insperation from this,
            #but you will need to impliment a state machine similar to what you made in lab 2 (including a way of counting time without blocking)
            if (now - old) > .0001: # check if time stamp differs by interval
                old = now ## update timestamp for last iteration of this if
                if z == 0:
                    print('ERROR: DETECT NO LINE????')
                    ### REVISIT THIS SECTION ### will need to prepare for this case. seek line?
                    
                elif  z > 7000: #im assuming that in your arduino code you will be setting z to the int 8000 if you sense a cross, dont feel obligated to do it this way.  
                    # now that we are SURE that z isnt the string cross, we cast z to an int and recalculate leftMotor and rightMotor, 
                    ## move left (not pivot in place)
                    # do something here like incrimenting a value you call 'lines_hit' to one higher, and writing code to make sure that some time (1 second should do it) 
                    # passes between being able to incriment lines_hit so that it wont be incrimented a bunch of times when you hit your first cross. IE give your robot time to leave a cross
                    # before allowing lines_hit to be incrimented again.
                    print('AT INTERSECTION')
                    
                    cross_time_new = time.time() # constantly reassign time for checking intersection
                    if (cross_time_new - cross_time_old) > 1: # check if time elapsed since last intersection > 1 SECOND
                        cross_time_old = cross_time_new # reassign for time of last intersection
                        num_intersections +=1 # increment number of intersections
                        
                    if num_intersections == 2:
                        # pivot right (CW) then move straight
                        leftMotor = 200 
                        rightMotor = -200
                        break
                    elif num_intersections == 3:
                        # stop moving then pivot left (CCW)
                        leftMotor = -200
                        rightMotor = 200
                        
                        # reset num_intersections
                        num_intersections = 0
                        break
                    else:
                        # num_intersections is 1
                        # continue moving forward
                        leftMotor = 250
                        rightMotor = 250
                        
                elif z < 1500:
                    print('DETECT RIGHT, MOVING LEFT')
                    ## movin_waitinge left (not pivot in place)
                    leftMotor = 100 + 0.02 * z  
                    rightMotor = 250 - 0.02 * z
                                        
                elif z > 5500:
                    print('DETECT LEFT, MOVING RIGHT')
                    ## move right (not pivot in place)
                    leftMotor = 250 - 0.02*z  
                    rightMotor = 100 + 0.02*z
                    
                else:
                    print('DETECT CENTER - STRAIGHT')
                    ## move straight
                    leftMotor = 250
                    rightMotor = 250
                    
# def turnRight(initLeftEnc, initRightEnc):
#     leftEncDiff = 0
#     rightEncDiff = 0
#     print('am i in?')
#     while leftEncDiff < 90 and rightEncDiff < 90:
#         print('im in')
#         if ser.in_waiting > 0:
#                 line = ser.readline().decode('utf-8')
#                 #print(line)
#                 line=line.split(',')
#                 leftEncDiff = line[0] - initLeftEnc
#                 rightEncDiff = line[1] - initRightEnc
#                 time.sleep(0.3)
#                 print('hahahahahahha')

# line = ser.readline().decode('utf-8')
#                 #print(line)
# line=line.split(',')
# print(line)
# turnRight(line[0],line[1])   
                    
                        
                    
                    
                    
