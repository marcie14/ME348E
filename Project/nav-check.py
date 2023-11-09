#### V2 

'''##### import required libraries #####'''
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino
# import RPi.GPIO as GPIO # for IR sensor # commented out for debug on MAC


'''##### initialize setup variables  #####'''
### serial communications
# port = '/dev/ttyACMO' # RPi port for communicating to arduino board
port = '/dev/cu.usbmodem2101' # marcie mac port


'''##### initialize GPIO #####'''
### IR sensors
L_IR_pin = 4
M_IR_pin = 17
R_IR_pin = 18


'''##### initialize global variables #####'''
### time calculations
now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions
oldTurn = 0
interval = 0.05

### IR sensors
L_IR = -1
M_IR = -1
R_IR = -1
IR = [L_IR, M_IR, R_IR] # IR list

### ultrasonic variables
x_dist = -1 # distance x sensor detects from wall
y_dist = -1 # distance y sensor detects from wall
sendX = 83 # cm to send to arduino
sendY = 41 # cm to send to arduino
ultra_x_tol = 10   # (cm) ultrasonic sensor tolerance (x direction)
ultra_y_tol = 3    # (cm) ultrasonic sensor tolerance (y direction)
wallScan = []
frontWall = -1
left_position = -1
## GOAL LOCATIONS ##
shoot_y_dist = 41 # cm
leftGoal = (38, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
midGoal = (91, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
rightGoal = (57, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS

### Game MODE variables
MODE = 0 # for determining setup vs game mode

### serial communications variables
driveAction = -1 #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
feedAction = -1
shootAction = -1
String2Send='<'+str(driveAction)+',' + str(feedAction)+','+str(shootAction)+ '>'





'''############### MAIN FUNCTION ###############'''

if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.
    ser.reset_output_buffer()
    print('inif')
    
    while True:
        ser.write(String2Send.encode('utf-8'))
        sendString(port,115200,'<'+str(driveAction)+','+str(sendX)+','+str(sendY)+','+ str(feedAction)+','+str(shootAction)+ '>',0.0001)
        now = time.time() # constantly reassign new timestamp
        # print('in while')
        try:
            line = ser.readline().decode('utf-8')  # read incoming string
            line=line.split(',') # split incoming string into list with comma delimeter
            x_dist = float(line[0]) # distance x sensor detects from wall
            y_dist = float(line[1]) # distance y sensor detects from wall
            print(x_dist, y_dist)

        except UnicodeDecodeError:
            print("Received invalid byte sequence. Skipping...")
        except:
            print("packet dropped")
        
        if MODE == 0:
            # rotate 360 and scan walls, find furthest wall
            # orient towards IR sensors
        elif MODE == 1:
            
        if (y_dist < sendY): 
            stopMoving();
        
        elif (x_dist == -1):
            stopMoving();
        
        elif (x_dist < sendX - x_tol):# center 75, left 20, right 130
            turnRight();
        
        elif (x_dist > sendX + tol): # center 90, left 32, right 140
            turnLeft();
        
        else:
            moveStraight();
        