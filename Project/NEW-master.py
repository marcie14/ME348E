#### V2 
         
'''##### import required libraries #####'''
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
from sendStringScript import sendString # for communicating with arduino
import RPi.GPIO as GPIO # for IR sensor # commented out for debug on MAC
import random # for randomizing actions
from pynput.keyboard import Key, Controller # for debug
keyboard = Controller() # for debug

'''##### initialize setup variables  #####'''
### serial communications
port = '/dev/ttyACM0' # RPi port for communicating to arduino board
# port = '/dev/cu.usbmodem2101' # marcie mac port


'''##### initialize GPIO #####'''
### IR sensors
L_IR_pin = 4
M_IR_pin = 17
R_IR_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(L_IR_pin, GPIO.IN)
GPIO.setup(M_IR_pin, GPIO.IN)
GPIO.setup(R_IR_pin, GPIO.IN)


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

### Limit Switches
f_prime_switch = -1
f_drop_switch = -1
shoot_switch = -1

### Game MODE variables
MODE = 0 # for determining setup vs game mode

### serial communications variables
# rcvd_driveAction = -1 # received from arduino FOR DEBUG
# rcvd_feedAction = -1 # received from arduino FOR DEBUG
# rcvd_shootAction = -1 # received from arduino FOR DEBUG
# driveAction = 0 #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
# feedAction = 1
# shootAction = 0

''' new alyssa '''
# def alyssa():
#     currentX = 0
#     currentY = 0
#     currentTheta = 0
#     # % dt = sampling period
#     # % d = diameter of wheel
#     # % encR = number of encoder pulses of right wheel currently
#     # % encL = number of encoder pulses of left wheel currently
#     # % pprR = pulses per revolution for right motor
#     # % pprL = pulses per revolution for left motor
#     while tcurr < tstop
#         omegaLeft = 2*pi*encL/(pprL*tcurr)
#         omegaRight = 2*pi*encR/(pprR*tcurr)
#         vL = omegaLeft*d/2
#         vR = omegaRight*d/2

#         currentTheta = (1/l)*(vR-vL)*dt
#         currentX = currentX + 0.5*(vR + vL)*cos(currentTheta)*dt
#         currentY = currentY + 0.5*(vR + vL)*sin(currentTheta)*dt




'''############### MAIN FUNCTION ###############'''

if __name__ == '__main__':
    ser=serial.Serial(port,baudrate=115200)
    ser.reset_input_buffer() #clears anything the arduino has been sending while the Rpi isnt prepared to recieve.
    ser.reset_output_buffer()
    
    
    print('INITIALIZE FIRST MOVES') # for debug
    #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
    driveAction = input('driveAction: ') # for debug
    feedAction = input('feedAction: ') # for debug # 1 = prime, 2 = drop
    shootAction = input('shootAction: ') # for debug # 0 = stop, 1 = shoot
    String2Send='<'+str(driveAction)+','+str(sendX)+','+str(sendY)+','+ str(feedAction)+','+str(shootAction)+ '>'

    while True:
        ser.write(String2Send.encode('utf-8'))
        sendString(port,115200,'<'+str(driveAction)+','+str(sendX)+','+str(sendY)+','+ str(feedAction)+','+str(shootAction)+ '>',0.0001)
        now = time.time() # constantly reassign new timestamp
        # print('in while') # for debug

        try:
            line = ser.readline().decode('utf-8')  # read incoming string
            line=line.split(',') # split incoming string into list with comma delimeter
            # print(line)
            # x_dist = float(line[0]) # distance x sensor detects from wall
            # y_dist = float(line[1]) # distance y sensor detects from wall
            L_IR = GPIO.input(L_IR_pin)
            M_IR = GPIO.input(M_IR_pin)
            R_IR = GPIO.input(R_IR_pin)
        
            left = float(line[0])
            right = float(line[1])
            front = float(line[2])
            back = float(line[3])
            f_prime_switch = int(line[4])
            f_drop_switch = int(line[5])
            shoot_switch = int(line[6])
            rcvd_driveAction = int(line[7])
            rcvd_feedAction = int(line[8])
            rcvd_shootAction = int(line[9])

            print('ultrasonics: ' + str(left) + ',' + str(right) +',' + str(front) + ',' + str(back))
            print('limit switches: ' + str(f_prime_switch) + ',' + str(f_drop_switch) + ',' + str(shoot_switch))
            print('recieved: ' + str(rcvd_driveAction) + ',' + str(rcvd_feedAction) + ',' + str(rcvd_shootAction))
            time.sleep(0.5)

        except UnicodeDecodeError:
            print("Received invalid byte sequence. Skipping...")
        except:
            print("packet dropped")
            # GPIO.cleanup()
        
        ## shoot sequence 
        if f_prime_switch == 1: # if primed
            feedAction = 2 # drop
        if f_drop_switch == 1: # if dropped
            feedAction = 0 # stop feeder
            shootAction = 1 # shoot

        ## prime sequence
        if (shoot_switch == 1) and (f_drop_switch == 1): # if shoot switch pressed (at threshold)
            shootAction = 0 # stop shoot
            feedAction = 1 # prime


        #### below is commented out because the IR is not integrated yet
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


        # IR = [L_IR, M_IR, R_IR] # IR list
        # MODE = 1

        
       
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
        #         if (front < sendY): 
        #             driveAction = -1 # stop moving
                
        #         elif (sendX - ultra_x_tol <= left <= sendX + ultra_x_tol):
        #             driveAction = 0 # forward
                
        #         elif (left < sendX - ultra_x_tol):# center 75, left 20, right 130
        #             driveAction = 1 # left
                
        #         elif (left > sendX + ultra_x_tol): # center 90, left 32, right 140
        #             driveAction = 2 # right
            
        #         else:
        #             driveAction = 0 # forward
        #     else:
        #         print('no IR')

                