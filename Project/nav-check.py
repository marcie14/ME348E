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
ultra_tol = 3.00   # (cm) ultrasonic sensor tolerance
wallScan = []
frontWall = -1
left_position = -1
## GOAL LOCATIONS ##
shoot_y_dist = 30 # cm
G1 = (38, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
G2 = (91, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
G3 = (57, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS

### Game MODE variables
MODE = 0 # for determining setup vs game mode

### serial communications variables
driveAction = -1
shootAction = -1
feedAction = -1
String2Send='<'+str(driveAction)+','+str(shootAction)+ ',' + str(feedAction)+'>'

if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.
    # ser.reset_output_buffer()
    
    while True:
        sendString(port,115200,'<'+str(driveAction)+','+str(shootAction)+ ',' + str(feedAction)+'>',0.0001)
        # L_Motor, R_Motor, Feeder, Shooter
        now = time.time() # constantly reassign new timestamp
        # ser.write(String2Send.encode('utf-8'))
        print('in true')
        if ser.in_waiting > 0:  #we wait until the arduino has sent something to us before we try to read anything from the serial port.
            line = ser.readline().decode('utf-8') # read incoming string
            line=line.split(',') # split incoming string into list with comma delimeter
            print(line)