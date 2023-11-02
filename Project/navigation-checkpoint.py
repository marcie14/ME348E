#!/usr/bin/env python3

##### import libraries #####
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino
import RPi.GPIO as GPIO # for IR sensor

##### set up variables #####
port = '/dev/ttyACM0' # RPi port for communicating to arduino board
# port = '/dev/cu.usbmodem2101' # marcie mac port

now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions

# set initial values
x_dist = -1 # distance x sensor detects from wall
y_dist = -1 # distance y sensor detects from wall
ultra_tol = 3.00   # ultrasonic sensor tolerance
direction = '' # what direction bot is facing

# leftMotor=int(100)
# rightMotor=int(100)
L_Motor = 100
R_Motor = 100
motors = (L_Motor, R_Motor) # motor tuple

# IR sensors
L_IR_pin = 17
M_IR_pin = 18
R_IR_pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(L_IR_pin,GPIO.IN)
GPIO.setup(M_IR_pin,GPIO.IN)
GPIO.setup(R_IR_pin,GPIO.IN)


print('IR Sensor Ready')
print()

L_IR = -1
M_IR = -1
R_IR = -1
IR = [L_IR, M_IR, R_IR] # IR list

MODE = 0 # for determining setup vs game mode
G1 = (38, 30) # cm - NOT ADJUSTED FOR CHASSIS
G2 = (91, 30) # cm - NOT ADJUSTED FOR CHASSIS
G3 = (57, 30) # cm - NOT ADJUSTED FOR CHASSIS

def get_dir(x, y):
    dir = 1
    return dir

String2Send='<250,250>'

##########
if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.
    ser.reset_output_buffer()

    while True:
        # sendString(port,115200,'<'+str(L_Motor)+','+str(R_Motor)+'>',0.0001)
        # L_Motor, R_Motor, Feeder, Shooter
        now = time.time() # constantly reassign new timestamp
        ser.write(String2Send.encode('utf-8'))
        sendString(port,115200,'<250, -250>',0.0001) #turn right motor command here
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            print('in if ser waiting')
            line = ser.readline().decode('utf-8') # read incoming string
            # print(line) # debug

            line=line.split(',') # split incoming string into list with comma delimeter
            print(line) # debug

            try:
                print('in try')
                x_dist = float(line[0]) # distance x sensor detects from wall
                y_dist = float(line[1]) # distance y sensor detects from wall
                # L_Motor = int(line[2]) # left motor speed
                # M_Motor = int(line[3]) # right motor speed

                # L_IR = GPIO.input(L_IR_pin) # left IR sensor reading
                # M_IR = GPIO.input(M_IR_pin) # middle IR sensor reading
                # R_IR = GPIO.input(R_IR_pin) # right IR sensor reading

                # motors = (L_Motor, R_Motor) # motor tuple
                # IR = [L_IR, M_IR, R_IR] # IR list - NOT DETECTED == [1,1,1]

                print(x_dist, y_dist)
                # direction = get_dir(x_dist, y_dist)
            except:
                print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 
                GPIO.cleanup()

            if MODE == 0:
                # rotate 360 deg to orient system
                # set dir = front sensor detects front wall, left to left
                # move forward to G2 = (x,y)
                MODE == 1
            elif MODE == 1:
                # detect IR sensor. L,M,R
                if IR == [1,0,0] or IR == [1,1,0]:
                    print('ir detected on left')
                    # pivot 90 deg CCW
                    # move forward until hit G1 or G2 with tolerance
                    # pivot 90 deg CW
                    # validate IR reading and G1 or G2 location
                    # shoot
                elif IR == [0,1,0]:
                    print('ir detected center')
                    # shoot
                elif IR == [0,1,1] or IR == [0,0,1]:
                    print('ir detected on right')
                    # pivot 90 deg CW
                    # move forward until hit G2 or G3 with tolerance
                    # pivot 90 deg CCW
                    # validate IR reading and G1 or G2 location
                    # shoot
                else: ## [0,0,0] or [1,0,1]
                    print('no ir detected...')
                    # ERROR or game over
                
           