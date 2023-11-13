#### V2 

'''##### import required libraries #####'''
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino
# import RPi.GPIO as GPIO # for IR sensor # commented out for debug on MAC
import random # for randomizing actions
from pynput.keyboard import Key, Controller # for debug
keyboard = Controller() # for debug

'''##### initialize setup variables  #####'''
### serial communications
# port = '/dev/ttyACMO' # RPi port for communicating to arduino board
port = '/dev/cu.usbmodem2101' # marcie mac port


'''##### initialize GPIO #####'''
### IR sensors
L_IR_pin = 4
M_IR_pin = 17
R_IR_pin = 18
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(L_IR_pin, GPIO.IN)
# GPIO.setup(M_IR_pin, GPIO.IN)
# GPIO.setup(R_IR_pin, GPIO.IN)


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
# x_dist = -1 # distance x sensor detects from wall
# y_dist = -1 # distance y sensor detects from wall
left = -1 # distance left sensor detects from wall
right = -1 # distance right sensor detects from wall
front = -1 # distance front sensor detects from wall
back = -1 # distance back sensor detects from wall
sendX = 83 # cm to send to arduino
sendY = 41 # cm to send to arduino
ultra_x_tol = 10   # (cm) ultrasonic sensor tolerance (x direction)
ultra_y_tol = 3    # (cm) ultrasonic sensor tolerance (y direction)
wallScan = []
frontWall = -1
left_position = -1
## GOAL LOCATIONS ##
shoot_y_dist = 41 # cm
leftGoal = (25, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
midGoal = (83, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS
rightGoal = (135, shoot_y_dist) # cm - NOT ADJUSTED FOR CHASSIS

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
    
    
    print('inif') # for debug
    #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
    driveAction = input('driveAction: ') # for debug
    feedAction = input('feedAction: ') # for debug
    shootAction = input('shootAction: ') # for debug
    
    while True:
        ser.write(String2Send.encode('utf-8'))
        sendString(port,115200,'<'+str(driveAction)+','+str(sendX)+','+str(sendY)+','+ str(feedAction)+','+str(shootAction)+ '>',0.0001)
        now = time.time() # constantly reassign new timestamp
        # print('in while') # for debug

        try:
            line = ser.readline().decode('utf-8')  # read incoming string
            line=line.split(',') # split incoming string into list with comma delimeter
            x_dist = float(line[0]) # distance x sensor detects from wall
            y_dist = float(line[1]) # distance y sensor detects from wall
            L_IR = GPIO.input(L_IR_pin)
            M_IR = GPIO.input(M_IR_pin)
            R_IR = GPIO.input(R_IR_pin)
            print('x: '+ x_dist + ', y:' +  y_dist + ', LIR: ' + L_IR + ', MIR: ' + M_IR + ', RIR: ' + R_IR)


        except UnicodeDecodeError:
            print("Received invalid byte sequence. Skipping...")
        except:
            print("packet dropped")
            # GPIO.cleanup()
        
        # if GPIO.input(L_IR_pin) == 0:
        #     L_IR = 0 # IR sensor detects something! (active low)
        # else:
        #     L_IR = 1
        # if GPIO.input(M_IR_pin) == 0:
        #     M_IR = 0 # IR sensor detects something! (active low)
        # else:
        #     M_IR = 1
        # if GPIO.input(R_IR_pin) == 0:
        #     R_IR = 0 # IR sensor detects something! (active low)
        # else:
        #     R_IR = 1

        # L_IR = random.randint(0,1)
        # M_IR = random.randint(0,1)
        # R_IR = random.randint(0,1)
        # IR = [L_IR, M_IR, R_IR] # IR list
        # MODE = 1
        
        #### below 
        # if MODE == 0:
            
        #     driveAction = 2 # rotate right
        #     startTurn = now
            
        #     if startTurn - oldTurn > 5:
        #         oldTurn = startTurn
        #         MODE = 1
        #     MODE = 1
        #     # orient towards IR sensors
        #     # move forward to shoot_y_dist
        #     break
            
        # elif MODE == 1:
        #     # check for LMR IR sensors
        #     if IR == 0: # if IR sensor detects something
        #         # move forward
        #         driveAction = 0
                
        #         #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
        #         if IR == [1,0,0] or IR == [1,1,0]:
        #             print('ir detected on left')
        #             sendX = leftGoal[0]
        #             sendY = leftGoal[1]
        #         elif IR == [0,1,0]:
        #             print('ir detected center')
        #             sendX = midGoal[0]
        #             sendY = midGoal[1]
                    
        #         elif IR == [0,1,1] or IR == [0,0,1]:
        #             print('ir detected on right')
        #             sendX = rightGoal[0]
        #             sendY = rightGoal[1]
                    
        #         ### execute driveAction
        #         if (y_dist < sendY): 
        #             driveAction = -1 # stop moving
                
        #         elif (sendX - ultra_x_tol <= x_dist <= sendX + ultra_x_tol):
        #             driveAction = 0 # forward
                
        #         elif (x_dist < sendX - ultra_x_tol):# center 75, left 20, right 130
        #             driveAction = 1 # left
                
        #         elif (x_dist > sendX + ultra_x_tol): # center 90, left 32, right 140
        #             driveAction = 2 # right
            
        #         else:
        #             driveAction = 0 # forward
        #     else:
        #         print('no IR')