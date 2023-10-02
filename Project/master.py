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
            
            line = ser.readline().decode('utf-8')
            # print(line)

            #this splits the incoming string up by commas
            line=line.split(',')
            try:
                x = int(line[0])
                y = int(line[1])
                z = int(line[2]) # we dont convert this to a float becasue we went to be able to recieve the message that we are at a cross, which wont be an int. 
                # print([x,y,z])
                # print(now)
                # print(old)
                
            except:
                print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 


            if (now - old) > .0001: # check if time stamp differs by interval
                old = now # update timestamp for last iteration of this if
                if z == 0:
                    print('ERROR: DETECT NO LINE????')
                    ### REVISIT THIS SECTION ### will need to prepare for this case. seek line?
                    
                elif not z < 7000: #im assuming that in your arduino code you will be setting z to the int 8000 if you sense a cross, dont feel obligated to do it this way.  
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
                    
                        
                    
                        
                    
                    
                    
