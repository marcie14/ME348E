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
BUMPS = [-1,-1,-1,-1,-1,-1]   # array of values, will be 0 if has been pushed

MODE = 0 # for determining setup vs game mode
    

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
        
            except:
                print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 
                
            if BUMPS != [-1,-1,-1,-1,-1,-1] or BUMPS != [1,1,1,1,1,1]:  # if has been bumped
                # run bump function
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
                
                elif -1 in BUMPS[0:6]:
                    print('not receiving BUMPS')

                else:
                    # print('keep driving')
                    String2Send='<-200,200>'
                    sendString(port,115200,String2Send,0.0005)

                # reassign old time and new time
                newt = time.time()

            elif MODE == 0:
                # navigate to front of arena
                print('1')
            elif MODE == 1:
                # game play mode
                print('1')
            else: # MODE == 2
                print('Game Over')


       
                
              
                        
                    
                        
                    
                    
                    
