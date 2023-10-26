#!/usr/bin/env python3

##### import libraries #####
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino

##### set up variables #####
# port = '/dev/ttyACM0' # RPi port for communicating to arduino board
port = '/dev/cu.usbmodem2101' # marcie mac port

now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions

# leftMotor=int(100)
# rightMotor=int(100)
leftMotor = 100
rightMotor = 100


# set initial values
x_dist = -1 # distance x sensor detects from wall
y_dist = -1 # distance y sensor detects from wall


MODE = 0 # for determining setup vs game mode
    

##########
if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.

    while True:
        sendString(port,115200,'<'+str(leftMotor)+','+str(rightMotor)+'>',0.0001)
        
        now = time.time() # constantly reassign new timestamp
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            
            line = ser.readline().decode('utf-8') # read incoming string
            # print(line) # debug

            line=line.split(',') # split incoming string into list with comma delimeter
            try:
                x_dist = int(line[0]) # distance x sensor detects from wall
                y_dist = int(line[1]) # distance y sensor detects from wall
                print(x_dist, y_dist)
            except:
                print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 
                
           