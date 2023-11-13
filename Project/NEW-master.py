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
# port = '/dev/ttyACM0' # RPi port for communicating to arduino board
port = '/dev/cu.usbmodem142101' # brycen mac port




'''##### initialize GPIO #####'''
### IR sensors
L_IR_pin = 17
M_IR_pin = 27
R_IR_pin = 22
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(L_IR_pin, GPIO.IN)
# GPIO.setup(M_IR_pin, GPIO.IN)
# GPIO.setup(R_IR_pin, GPIO.IN)




'''##### initialize global variables #####'''
### time calculations
now = time.time() # stores time for changing motor actions constantly updates
old = 0           # stores time since last change in motor actions
prevTurn = 0
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
diffX = []
single_DiffX = -1
diffY = []
single_DiffY = -1
frontWall = -1
left_position = -1
turnLeft = False
latch = 0
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
MODE = 0 # 0 = orient, 1 = scan for IR, 2 = orient and shoot
step = 0 # further increments each mode
### serial communications variables
# rcvd_driveAction = -1 # received from arduino FOR DEBUG
# rcvd_feedAction = -1 # received from arduino FOR DEBUG
# rcvd_shootAction = -1 # received from arduino FOR DEBUG
driveAction = 4 #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
feedAction = 0
shootAction = 0


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
   # driveAction = input('driveAction: ') # for debug
   # feedAction = input('feedAction: ') # for debug # 1 = prime, 2 = drop
   # shootAction = input('shootAction: ') # for debug # 0 = stop, 1 = shoot
   MODE = int(input('Mode: ')) # for debug # 0 = orient, 1 = navigate to IR, 2 = shoot


   while True:
       String2Send='<'+str(driveAction)+','+ str(feedAction)+','+str(shootAction)+ '>'
       ser.write(String2Send.encode('utf-8'))
       sendString(port,115200,String2Send,0.0001)
       now = time.time() # constantly reassign new timestamp
       # print('in while') # for debug


       try:
           line = ser.readline().decode('utf-8')  # read incoming string
           line=line.split(',') # split incoming string into list with comma delimeter
           # print(line)
           # x_dist = float(line[0]) # distance x sensor detects from wall
           # y_dist = float(line[1]) # distance y sensor detects from wall
        #    L_IR = GPIO.input(L_IR_pin) # active low, 0 = detected
        #    M_IR = GPIO.input(M_IR_pin) # active low, 0 = detected
        #    R_IR = GPIO.input(R_IR_pin) # active low, 0 = detected
      
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
           #print('IR: ' + str(L_IR) + ',' + str(M_IR) +',' + str(R_IR))
           #print('limit switches: ' + str(f_prime_switch) + ',' + str(f_drop_switch) + ',' + str(shoot_switch))
           print('recieved: ' + str(rcvd_driveAction) + ',' + str(rcvd_feedAction) + ',' + str(rcvd_shootAction))
           time.sleep(0.5)


       except UnicodeDecodeError:
           print("Received invalid byte sequence. Skipping...")
       except:
           print("packet dropped")
           # GPIO.cleanup()
      
       ## shoot sequence
    #    if f_prime_switch == 1: # if primed
    #        feedAction = 2 # drop
    #    if f_drop_switch == 1: # if dropped
    #        feedAction = 0 # stop feeder
    #        shootAction = 1 # shoot


       ## prime sequence
    #    if (shoot_switch == 1) and (f_drop_switch == 1): # if shoot switch pressed (at threshold)
    #        shootAction = 0 # stop shoot
    #        feedAction = 1 # prime

        


       #### below is commented out because the IR is not integrated yet




       IR = [L_IR, M_IR, R_IR] # IR list


       print('MODE = ' + str(MODE))
       print('step = ' + str(step) + '\n\n')

       
      
     
       if MODE == 0: # orient bot towards front
           shootAction = 3
           if (front/back) > 5 and latch == 0:
              latch = 1
              step = 0
              int_diffX = abs(left-right)
           elif( latch == 0):
               step = 1
   
           if step == 0: # first step of MODE 0 - wall scan and detect squared position
            curr_diffX = abs(left-right)
            driveAction = 4
            print("sq")
            if(abs(curr_diffX - int_diffX) > ultra_x_tol):
               step = 1
            elif(abs(front - sendY) < ultra_y_tol):
               driveAction = 0 # stop moving
               MODE = 1
               step = 0
               print('done')
               break

            if step == 1: # second step of MODE 0 - begin rotating to find squared position
               driveAction = 2
##               if(right > left):
##                  driveAction = 2 # rotate right
##               else:
##                  driveAction = 1
##                  turnLeft = True
               #if (abs(now - prevTurn) > 0.01): # only run every 0.5 s
                #   prevTurn = now
               print("main")
               curr_diffX = [abs(left-right)] # difference between L and R ultrasonic
               diffX = diffX + curr_diffX # add to list difference between L and R ultrasonic
               squareX = min(diffX)
               curr_diffY = [front - back] # difference between L and R ultrasonic
               diffY = diffY + curr_diffY # add to list difference between L and R ultrasonic
               squareY = max(diffY)
               if (curr_diffX[0] > squareX + ultra_x_tol) and (curr_diffY[0] < squareY - ultra_y_tol):
                  
                   driveAction = 0 # stop moving
                   step = 2
          
           if step == 2: # third step of MODE 0 - set squared position, begin rotating back to squared position
               if(turnLeft):
                  driveAction = 2
               else:
                  driveAction = 1 # rotate left
               step = 3


           if step == 3: # fourth step of MODE 0 - stop moving once returned to squared position
               #if (abs(now - prevTurn) > 0.5): # only run every 0.5 s
                #   prevTurn = now
               single_DiffX = abs(left-right)
               single_diffY = front - back
               if (abs(single_DiffX - squareX) < ultra_x_tol) or (abs(single_DiffY - squareY) < ultra_y_tol): # if we are back to the point where diffX is at min (incl tolerance)
                  driveAction = 4 # stop moving
                  step = 4


           if step == 4: # fifth step of MODE 0 -  move forward until reach set y distance
               #if (abs(now - old) > 0.5): # only run every 0.5 s
                #   old = now
               if (abs(front - sendY) < ultra_y_tol): # while the front sensor is not the same as the set Y distance (incl tolerance)
                  driveAction = 4 # move straight
               else:
                  driveAction = 0 # stop moving
                  MODE = 1
                  step = 0
                  print('done')
                  break
          
           # orient towards IR sensors
           # move forward to shoot_y_dist
          
       # elif MODE == 1: # roll across shoot distance, scan IR
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
       # elif MODE == 2: # detect IR, pivot to face forward, shoot, repivot
       #     print("shoot")




              