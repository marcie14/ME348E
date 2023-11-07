#!/usr/bin/env python3

##### import libraries #####
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino
# import RPi.GPIO as GPIO # for IR sensor # commented out for debug on MAC

##### set up variables #####
# port = '/dev/ttyACMO' # RPi port for communicating to arduino board
port = '/dev/cu.usbmodem101' # marcie mac port

now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions
oldTurn = 0
interval = 0.05

# set initial values
x_dist = -1 # distance x sensor detects from wall
y_dist = -1 # distance y sensor detects from wall
ultra_tol = 3.00   # ultrasonic sensor tolerance
direction = '' # what direction bot is facing

wallScan = []
frontWall = -1
left_position = -1
driveAction = -1
shootAction = -1
feedAction = -1

# leftMotor=int(100)
# rightMotor=int(100)
# L_Motor = 100
# R_Motor = 100
# motors = (L_Motor, R_Motor) # motor tuple

# IR sensors
L_IR_pin = 4
M_IR_pin = 17
R_IR_pin = 18
# GPIO.setmode(GPIO.BCM) ## commented out for debug on MAC
# GPIO.setup(L_IR_pin,GPIO.IN)
# GPIO.setup(M_IR_pin,GPIO.IN)
# GPIO.setup(R_IR_pin,GPIO.IN)


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
position_tolerance = 3 # cm 
shoot_y_distance = 30 # cm, not adjusted for chassis

def get_dir(x, y):
    dir = 1
    return dir

String2Send='<'+str(driveAction)+','+str(shootAction)+ ',' + str(feedAction)+'>'
print('setup')
##########
if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.
    ser.reset_output_buffer()
    print('inif')
    while True:
        sendString(port,115200,'<'+str(driveAction)+','+str(shootAction)+ ',' + str(feedAction)+'>',0.0001)
        # L_Motor, R_Motor, Feeder, Shooter
        now = time.time() # constantly reassign new timestamp
        ser.write(String2Send.encode('utf-8'))
        sendString(port,115200,String2Send,0.0001) #turn right motor command here
        print('intrue')
        
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            print('in if ser waiting')
            if abs(old-now) >= interval:
                old = now
                print('in interval')
                line = ser.readline().decode('utf-8') # read incoming string
                # print(line) # debug

                line=line.split(',') # split incoming string into list with comma delimeter
                print(line) # debug

                try:
                    print('in try')
                    x_dist = float(line[0]) # distance x sensor detects from wall
                    y_dist = float(line[1]) # distance y sensor detects from wall
                    # L_Motor = int(line[2]) # left motor speed
                    # R_Motor = int(line[3]) # right motor speed

                    # L_IR = GPIO.input(L_IR_pin) # left IR sensor reading
                    # M_IR = GPIO.input(M_IR_pin) # middle IR sensor reading
                    # R_IR = GPIO.input(R_IR_pin) # right IR sensor reading

                    # motors = (L_Motor, R_Motor) # motor tuple
                    IR = [L_IR, M_IR, R_IR] # IR list - NOT DETECTED == [1,1,1]

                    print('Position: ',x_dist, y_dist)
                    # print('Motor Values: ', motors)
                    # print('IR Values: ', IR, '\n\n')
                    # direction = get_dir(x_dist, y_dist)
                except:
                    print("packet dropped") # this is designed to catch when python shoves bits on top of each other. 
                    # GPIO.cleanup() # commented out for debug no MAC
                    # break

            if MODE == 0: # scan walls                
                driveAction = 2 # rotate right to scan walls
                startTurn = now # mark time when start turn to scan
                if abs(oldTurn-startTurn) < 60: # scan walls for 6 seconds
                    wallScan = wallScan + [y_dist]
                else:
                    driveAction = 0 # stop scanning walls if more than 6 seconds
                
                frontWall = max(wallScan)
                
                # set dir = front sensor detects front wall, left to left
                # move forward to G2 = (x,y)
                MODE == 1
                
                
                
            elif MODE == 1: # rotate towards front wall
                if y_dist < frontWall:
                    driveAction = 2
                elif y_dist > frontWall:
                    driveAction = 3
                else: ## y_dist == front wall
                    driveAction = 0
                    MODE = 2
                    break
                
                
                
            elif MODE == 2: # move forwards to shooting area
                if y_dist < shoot_y_distance:
                    driveAction = 1 # move forward
                else:
                    driveAction = 0 # stop moving
                    left_position = x_dist # save x position for next MODE
                    MODE = 3
                    break
                
                
                
            elif MODE == 3:
                # detect IR sensor. L,M,R
                step = 0
                if IR == [1,0,0] or IR == [1,1,0]:
                    print('ir detected on left')
                    if step == 0:
                        if not left_position - position_tolerance <= y_dist <= left_position + position_tolerance:
                            driveAction = 3 # turn left
                        else: # y_dist = left position
                            driveAction = 1 # move straight
                            step = 1
                    elif step == 1:
                        break
                        # if y_dist 
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
                
           