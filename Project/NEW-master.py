#### V2

'''
status update:
- ultrasonic cosine for mode1 (see modes -3. -4)

- drives forward if placed forward, in middle of field (95% confidence...)
- IR circuit is operational
- some skeleton code for rando orientation, not working well...
- MODE 3 AND 4 (ASSUMES PUCK SLIDE EMPTY AND NOT HIT ANY SWITCH. ENTER MODE 4 FIRST) - no need to drive forward to shoot

To do:
- need to figure out placed in rando orientation**************************
- need to integrate IR (pivot in place to aim at IR)***********************
'''
       
'''##### import required libraries #####'''
import serial       # for communicating with arduino
import time         # for non-blocking code
import numpy as np  # for calcs
import math # for calcs
from sendStringScript import sendString # for communicating with arduino
import RPi.GPIO as GPIO # for IR sensor # commented out for debug on MAC
import random # for randomizing actions
from pynput.keyboard import Key, Controller # for debug
keyboard = Controller() # for debug


'''##### initialize setup variables  #####'''
### serial communications
port = '/dev/ttyACM1' # RPi port for communicating to arduino board
# port = '/dev/cu.usbmodem142101' # brycen mac port
# port = '/dev/cu.usbmodem21101' # marcie mac port




'''##### initialize GPIO #####'''
### IR sensors
L_IR_pin = 17
M_IR_pin = 27
R_IR_pin = 22
# L_IR_pin = 11
# M_IR_pin = 13
# R_IR_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(L_IR_pin, GPIO.IN)
GPIO.setup(M_IR_pin, GPIO.IN)
GPIO.setup(R_IR_pin, GPIO.IN)




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
recent_IR = [] # log of last few IR values


### ultrasonic variables
# x_dist = -1 # distance x sensor detects from wall
# y_dist = -1 # distance y sensor detects from wall
left = -1 # distance left sensor detects from wall
right = -1 # distance right sensor detects from wall
front = -1 # distance front sensor detects from wall
back = -1 # distance back sensor detects from wall
sendX = 83 # cm to send to arduino
sendY = 41 # cm to send to arduino
ultra_x_tol = 40   # (cm) ultrasonic sensor tolerance (x direction)
ultra_y_tol = 25    # (cm) ultrasonic sensor tolerance (y direction)
diffX = []
single_DiffX = -1
diffY = []
single_DiffY = -1
frontWall = -1
left_position = -1
turnLeft = False
latch = 0
startY = 0
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
driveAction = 0 #  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
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
  


mode2_step = 0
mode2_shoot = 0
shoot_drive_old = 0
lastShoot = 0
LS = 0
mode1_DIR = 0 # -1 = left, 0 = front, 1 = right
avg_right = []
r1 = -1
avg_cos = []
cos = -1

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
			# L_IR = GPIO.input(L_IR_pin) # active low, 0 = detected ## uncomment for MA
			IR = GPIO.input(M_IR_pin) # active low, 0 = detected
			# R_IR = GPIO.input(R_IR_pin) # active low, 0 = detected
			# IR = [L_IR, M_IR, R_IR] # IR list
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

			# print values from 
			print('ultrasonics: ' + str(round(left)) + ',' + str(round(right)) +',' + str(round(front)) + ',' + str(round(back)))
			print('IR: ' + str(IR))
			print('limit switches: ' + str(f_prime_switch) + ',' + str(f_drop_switch) + ',' + str(shoot_switch))
			print('recieved: dr ' + str(rcvd_driveAction) + ', fe ' + str(rcvd_feedAction) + ', sh ' + str(rcvd_shootAction))
			# time.sleep(0.5)


		except UnicodeDecodeError:
			print("Received invalid byte sequence. Skipping...")
		except:
			print("packet dropped")
			GPIO.cleanup()

        


		print('MODE = ' + str(MODE)) # debug for below
		print('step = ' + str(step) + '\n\n') # debug for below



		# if MODE == -3: # TEST COSINE FUNCTION FOR MODE 1
		# 	driveAction = 0
		# 	avg_right = avg_right + [right] # get average of right sensor
		# 	if len(avg_right) >= 20:
		# 		driveAction = 2 #turn right
		# 		r1 = np.average(avg_right) # take average of vals
				
		# 		MODE = -4
		# elif MODE == -4:
		# 	cos = [math.cos(r1 / right)]
		# 	avg_cos = avg_cos + cos # get degrees has turned
		# 	print('r1: ' + str(r1))
		# 	print('cos: ' + str(cos))
		# 	if len(avg_cos) >= 5:
		# 		avg_cos.pop(0)
		# 	if (np.average(avg_cos) > 0.70) and (np.average(avg_cos) < 1.04):
		# 		print('has turned 30-60 deg')
		# 		driveAction = 0
		# 		MODE = -2
		if MODE == -3: # TEST COSINE FUNCTION FOR MODE 1
			driveAction = 0
			avg_right = avg_right + [left] # get average of right sensor
			if len(avg_right) >= 20:
				driveAction = 1 #turn right
				r1 = np.average(avg_right) # take average of vals
				
				MODE = -4
		elif MODE == -4:
			cos = [math.cos(r1 / left)]
			avg_cos = avg_cos + cos # get degrees has turned
			print('r1: ' + str(r1))
			print('cos: ' + str(cos))
			if len(avg_cos) >= 5:
				avg_cos.pop(0)
			if (np.average(avg_cos) > 0.70) and (np.average(avg_cos) < 1.04):
				print('has turned 30-60 deg')
				driveAction = 0
				MODE = -2





		elif MODE == -2: # do nothing, view print statements from pi
			driveAction = 0
			feedAction = 0
			shootAction = 0
			print('\n')
      
		elif MODE == -1: # send serial before ending program
			break

		elif MODE == 0: # orient bot towards front
			#driveAction = 4
			shootAction = 3
			int_diffX = abs(left-right)
			try:
				if (front/back) > 5 and latch == 0:
					latch = 1
					step = 1
					tempFront = front
					print('forward')
				elif(back/front) > 4 and latch == 0:
					latch = 1
					step = 0
					startY = front
					print('Backward')
				elif( latch == 0):
					step = 2
					latch = 1
					lunch = 0
			except:
				print("error: packet dropped, divide by zero")
				
				
			if step == -1: # DEBUG allows previous drive actions to send through loop before ending program 
				break #### REMOVE FOR FINAL VERSION ####
            
            
			if step == 0:
				print('step 0')
				driveAction = 2 # turn
			
				if (abs(left-right) <= int_diffX) and (front > 3*startY): # difference between left and right ultrasonic exceed the allowable tolerance
					driveAction = 0
					step = 1
					print("0 end: ",abs(left-right))
				# elif ((front - shoot_y_dist) <= ultra_y_tol): # ront ultrasonic reaches predefined distance form front wall
				# 	driveAction = 0 # stop moving
				# 	MODE = 1
				# 	step = 0
				# 	print('3')
				
					
	
			if step == 1: # first step of MODE 0 - wall scan and detect squared position
				print('step 1')
				curr_diffX = abs(left-right)
				driveAction = 3
				#print(front-sendY) < 5
				if(abs(curr_diffX) > left):#ultra_x_tol):
					step = 2
					print("1 end: ",curr_diffX)
					lunch = 0
				elif ((front-sendY) < 5): # changed from ultra_y_tol
					driveAction = 0 # stop moving
					# MODE = 1 # uncomment for final
					#step = 0
					print('done - step 1')
					MODE = -1 # DEBUG end program
					

			if step == 2: # second step of MODE 0 - begin rotating to find squared position
				print('step 2')
				# driveAction = 2
				if lunch == 0:
					if(right > left):
						driveAction = 2 # rotate right
						lunch = 1
					else:
						driveAction = 1
						turnLeft = True
						lunch = 1
				# if (abs(now - prevTurn) > 0.01): # only run every __ s
				# 	prevTurn = now
				curr_diffX = [abs(left-right)] # difference between L and R ultrasonic
				diffX = diffX + curr_diffX # add to list difference between L and R ultrasonic
				squareX = min(diffX)
				curr_diffY = [front - back] # difference between L and R ultrasonic
				diffY = diffY + curr_diffY # add to list difference between L and R ultrasonic
				squareY = max(diffY)
				if (curr_diffX[0] > squareX + ultra_x_tol): #or (curr_diffY[0] < squareY - ultra_y_tol):
					print('------------------------------------------------------------------------------------------------------------------------------------')
					driveAction = 0 # stop moving
					step = 3
		
			if step == 3: # third step of MODE 0 - set squared position, begin rotating back to squared position
				print('step 3')
				curr_diffX = [abs(left-right)] # difference between L and R ultrasonic
				if(turnLeft):
					driveAction = 2 #int_diffX
					print('turned right')
					if ((curr_diffX[0] > squareX + ultra_x_tol) and (front > 50)): #or (curr_diffY[0] < squareY - ultra_y_tol):
						# print('------------------------------------------------------------------------------------------------------------------------------------')
						driveAction = 0 # stop moving
						print('x squared - stop')
				else:
					driveAction = 1 # rotate left
					print('turned left')
				
				
				MODE = -1 # DEBUG, end program


			if step == 4: # fourth step of MODE 0 - stop moving once returned to squared position
				#if (abs(now - prevTurn) > 0.5): # only run every 0.5 s
					#   prevTurn = now
				print('step 4')
				single_DiffX = abs(left-right)
				single_diffY = abs(front - back)
				if (abs(single_DiffX - squareX) < ultra_x_tol):# or ((single_DiffY - squareY) < ultra_y_tol): # if we are back to the point where diffX is at min (incl tolerance)
					driveAction = 0 # stop moving
					step = 5


			if step == 5: # fifth step of MODE 0 -  move forward until reach set y distance
				#if (abs(now - old) > 0.5): # only run every 0.5 s
					#   old = now
				print('step 5')
				if (front > 20): # while the front sensor is not the same as the set Y distance (incl tolerance)
					driveAction = 3 # move straight
				else:
					driveAction = 0 # stop moving
					# MODE = 1 # uncomment for final
					step = 1
					print('done - step 5') ## debug - remove for final version
					# MODE = -1 # DEBUG end program
					## debug - remove for final version
		
  
    #### below is commented out because the IR is not integrated on robot yet
		elif MODE == 1: # scan IR, pivot towards "on"
			curr_IR = [IR]
			if len(recent_IR) >= 10:
				print('20')
				# remove first IR
				
				recent_IR.pop(0)
				recent_IR = recent_IR + curr_IR
			else: 
				print('too short')
				recent_IR = recent_IR + curr_IR

			if np.average(recent_IR) < 0.5:
				print("IR detected")
				driveAction = 0
				MODE = -2
				if mode2_DIR == 0:
					mode2_DIR = 1
				# if 

				# MODE = -1
				# MODE = 2
			elif (mode2_DIR == 0):
				print("not detected")
				driveAction = 2
				
				# MODE = -2 # DEBUG
			


		########################## BELOW IS OLD
		# 	driveAction = 1
	    # # check for LMR IR sensors
		# 	if IR == 0: # if IR sensor detects something
		# 		# move forward
		# 		driveAction = 0
				
		# 		#  0 = forward, 1 = left, 2 = right, 3 = backward, else = stop moving
		# 	if IR == [1,0,0] or IR == [1,1,0]:
		# 		print('ir detected on left')
		# 		sendX = leftGoal[0]
		# 		sendY = leftGoal[1]
		# 	elif IR == [0,1,0]:
		# 		print('ir detected center')
		# 		sendX = midGoal[0]
		# 		sendY = midGoal[1]
				
		# 	elif IR == [0,1,1] or IR == [0,0,1]:
		# 		print('ir detected on right')
		# 		sendX = rightGoal[0]
		# 		sendY = rightGoal[1]
					
	    #     	### execute driveAction
		# 		if (front < sendY):
		# 			driveAction = -1 # stop moving
		# 		elif (sendX - ultra_x_tol <= left <= sendX + ultra_x_tol):
		# 			driveAction = 0 # forward
				
		# 		elif (left < sendX - ultra_x_tol):# center 75, left 20, right 130
		# 			driveAction = 1 # left
				
		# 		elif (left > sendX + ultra_x_tol): # center 90, left 32, right 140
		# 			driveAction = 2 # right
			
		# 		else:
		# 			driveAction = 0 # forward
		# 	else:
		# 		print('no IR')

		elif MODE == 2: # VERIFY IR in front, feeder prime/drop, move forward, shoot, move back, go back to mode 1
			print("shoot")
			'''SHOOTING/FEEDING
				***ASSUMING WE START WITH NO SWITCHES HIT, NO PUCKS PRIMED***
				if feeder not primed, prime
			'''
			if mode2_step == 0: # if has not yet primed
				if (((f_drop_switch == 0) and (f_prime_switch == 0)) or (f_drop_switch == 1)): # if feeder slide is in middle or drop switch pressed
					feedAction = 1 # prime
				elif (f_prime_switch == 1): # if primed
					# feedAction = 0 # pause while primed until time to drop puck
					feedAction = 2 # drop
					mode2_step = 1 # has primed
					mode2_shoot = 0
			elif mode2_step == 1: # if has primed
				if ((f_drop_switch == 0) and (f_prime_switch == 0)): # if feeder slide is in middle
					feedAction = 2 # drop
				elif (f_drop_switch == 1): # if dropped
					feedAction = 0 # stop moving feeder
					if mode2_shoot == 0: # if in first section of shoot cycle
						driveAction = 3 # move straight
						if ((now - shoot_drive_old) > 2): #if has been driving straight for 2 sec
							driveAction = 0 # stop moving
							mode2_shoot = 1 # enter second mode of shoot cycle

					elif mode2_shoot == 1: # if second mode of shoot cycle
						if shoot_switch == 0: #  if shoot switch has not been pushed
							shootAction = 1 # shoot
							mode2_shoot = 2 # update action of been shot

					elif mode2_shoot == 2: # if third mode of shoot cycle
						if shoot_switch == 1: # if shoot switch has been pushed
							shootAction = 0 # stop shooting
							driveAction = 4 # move backwards
						if ((now - shoot_drive_old) > 2): #if has been driving backwards for 2 sec
							driveAction = 0 # stop moving
							mode2_step = 0 # reset variables for MODE 2
							mode2_shoot = 0 # reset variables for MODE 2

		elif MODE == 3: ## shoot mode 
			feedAction = 0
			if shoot_switch == 1:
				
				shootAction = 0
				# MODE = -1
				# if now - lastShoot > 50:
				# 	shootAction = 1
				# 	LS = 1
				feedAction = 1 # prime feeder
				MODE = 4

		elif MODE == 4: ## feed Mode
			shootAction = 0
			if f_prime_switch == 1: # if primed
				feedAction = 2 # drop
				
			elif f_drop_switch == 1: # if dropped
				feedAction = 0 # prime
				shootAction = 1
				MODE = 3

			
			###### OLD SHOOT BELOW
			# if (shoot_switch == 1):
			# 	shootAction = 0
			# 	# time.sleep(1)
			# 	if (f_prime_switch == 1):
			# 		feedAction = 2
					
			# 		step = 1
			# 	elif (f_drop_switch == 1):
			# 		feedAction = 1
			# 		shootAction = 1
					
			# 		step = 0
			# 	elif ((f_drop_switch == 0) and (f_prime_switch == 0)):
			# 		if step == 0:
			# 			feedAction = 1
						
			# 		else:
			# 			feedAction = 2
						

			# else:
			# 	shootAction = 1
			# 	step = 0
			
			'''END SHOOTING/FEEDING'''




			
	''' OLD shoot'''
	# # shoot sequence
	# if f_prime_switch == 1: # if primed
	# 	feedAction = 2 # drop
	# if f_drop_switch == 1: # if dropped
	# 	feedAction = 0 # stop feeder
	# 	shootAction = 1 # shoot


	# # prime sequence
	# if (shoot_switch == 1) and (f_drop_switch == 1): # if shoot switch pressed (at threshold)
	# 	shootAction = 0 # stop shoot
	# 	feedAction = 1 # prime
	'''END OLD shoot'''

	""" notes for MODE 0
		1. Check if front ultrasonic is ~5x the reading as the back ultrasonic
			If True, continue to step 2
			If False, skip to step 3b

		2. Drive forward and check that the difference between left and right ultrasonic stays roughly the same within some given tolerance. Continue driving forward until one of two conditions are met:
			a) Front ultrasonic reaches predefined distance form front wall
			b) Difference between left and right ultrasonic exceed the allowable tolerance

		3.
		If a) begin IR search and shooting
		If b) begin sweeping, rotating in the direction (left/ccw or right/cw) with the larger ultrasonic reading

	"""