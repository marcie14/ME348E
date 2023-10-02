#!/usr/bin/env python3

##### import libraries #####
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino

##### set up variables #####
port = '/dev/ttyACM0' # port for communicating to arduino board

now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions
cross_time_new = time.time() # stores time for checking intersections (constantly updates)
cross_time_old = 0           # stores time from last intersection
num_intersections = 0        # increments according to number of intersections 

leftMotor=int(100)
rightMotor=int(100)


# set initial values
x = -1 # left motor reading
y = -1 # right motor reading
z = -1 # line sensor reading

# bump sensors 
#a bump sensor that is unactivated starts at 1 (because they are pullups), hence why these are all one
FR=int(1)   # far right
R=int(1)    # right
MR=int(1)   # middle right
ML=int(1)   # middle left
L=int(1)    # left
FL=int(1)   # far left
BUMPS = [0,0,0,0,0,0]   # array of values, will not be 1 if has been pushed


def bumpSensors():
    return

def irSensors():
    return

def lineFollowing():
    return


##########
if __name__ == '__main__':
    ser=serial.Serial(port,115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.

    while True:
        sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0001)
        
        now = time.time() # constantly reassign new timestamp
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            
            line = ser.readline().decode('utf-8') # read incoming string
            # print(line) # debug

            line=line.split(',') # split incoming string into list with comma delimeter
            try:
                # line following 
                x = int(line[0]) # left motor
                y = int(line[1]) # right motor
                z = int(line[2]) # line detection
                
                # bump sensors
                FR=int(line[3]) # far right
                R=int(line[4])  # right
                MR=int(line[5]) # middle right

                ML=int(line[6]) # middle left
                L=int(line[7])  # left
                FL=int(line[8]) # far left

                BUMPS = [FL, L, ML, MR, R, FR] # array version of bump sensors from left to right
                # print('BUMPS: ', BUMPS) # debug
                # print('x, y, z: ', [x,y,z]) # debug
                # print('now: ', now) # debug
                # print('old: ', old) # debug
                
            except:
                print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 


            if (now - old) > .0001: # check if time stamp differs by interval
                old = now # update timestamp for last iteration of this if
                
                # if bump sensor has been pressed, run bump function.... but is this blocking?
                if BUMPS != [0,0,0,0,0,0]: 
                    bumpSensors(BUMPS)
                    
                elif (z != -1):
                    lineFollowing(z)
                    break
                
                if z == 0:
                    print('ERROR: DETECT NO LINE????')
                    ### REVISIT THIS SECTION ### will need to prepare for this case. seek line?
                    
                elif not z < 7000: #im assuming that in your arduino code you will be setting z to the int 8000 if you sense a cross, dont feel obligated to do it this way.  
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
                    ## move left (not pivot in place)
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
                    
                        
                    
                        
                    
                    
                    
