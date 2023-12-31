
#!/usr/bin/env python3
import serial
import time
import numpy as np
import RPi.GPIO as GPIO
from simple_pid import PID
from gpiozero import RotaryEncoder
#import matplotlib.pyplot as plt
# import pandas as pd

#assign parameter values
ppr = 48 #pulse per rev for encoder 
tsample = 0.1 # sampling period for encoder reading
tdisp = 0.1 # freqency to show encoder reading on terminal
tstop = 20

### idk what this is below
K = 0.2


T = 0.19
d = 0.05
k = 20

Gp = 2

#values for motor with without load on it
kp = 0
ki = 0
kd = 0
setPoint = 15

# pid = PID(Kp, Ki, Kd, setPoint)


#idk what this is above

ts = []
revs = []

# create encoder object on GPIO pins 17 and 18
encoder = RotaryEncoder(24, 25, max_steps=0)


# Define motor pins forward pin (in1) 22, backward (in2) 23, PWM (en) 24
in1 = 6
in2 = 5
en = 23


# initialize values
velCurr = 0
posCurr = 0
posLast = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()
lastSpeedError=0
cumError = 0
error = 0
rateError = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)
p=GPIO.PWM(en,100)
p.start(100)



print('running code for',tstop, 'seconds...')
print('turn encoder')

while tcurr <= tstop:
	time.sleep(tsample)
	tcurr = time.perf_counter()-tstart
	posCurr = encoder.steps
	velCurr = ((posLast-posCurr)/(tcurr-tprev))/ppr # in rev/sec
	if(10>tcurr>6):
		setPoint=16
	elif(tcurr>10):
		setPoint=12
	else:
		setPoint=15
	if(np.floor(tcurr/tdisp)-np.floor(tprev/tdisp))==1:
		# out = p.update(pid(velCurr))
		# p.start(abs(out))
		# error = setPoint-velCurr
		# cumError = cumError + error*(tdisp)
		# rateError = (error-lastSpeedError)/tdisp
		# out = kp*error + ki*cumError + kd*rateError
		# p.ChangeDutyCycle(out)
		# print(velCurr , out, tcurr)
		print(velCurr, tcurr)
		ts.append(tcurr)
		revs.append(velCurr)

	tprev = tcurr
	posLast = posCurr
	lastSpeedError = error


	## marcie comment below
	# inp =1
	# error = setPoint - inp
	# cumError += error*elapsed
	# rateError = cumError
	# vals.append(np.abs(velCurr))
	# ts.append(tcurr)
	# out = Kp*error + Ki*cumError + Kd*rateError
	## marcie comment above


# plt.plot(ts, revs)

	
print('Done.')
GPIO.cleanup()
encoder.close()




