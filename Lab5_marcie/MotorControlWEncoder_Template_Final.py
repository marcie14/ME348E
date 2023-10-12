#!/usr/bin/env python3
import serial
import time
import numpy as np
import RPi.GPIO as GPIO
from gpiozero import RotaryEncoder
# import pandas as pd

#assign parameter values
ppr = 48 #pulse per rev for encoder 
tsample = 0.02 # sampling period for encoder reading
tdisp = 0.5 # freqency to show encoder reading on terminal
tstop = 20

### idk what this is below
K = 0.2
deltaEffort = 1

T = 0
d = 0
Gp = K / deltaEffort

Kp = 1.2 * T / (d * Gp)
Ki = 0.5 / d
Kd = 0.5 * d

error = 1
cumError = error
rateError = cumError

out = Kp*error + Ki*cumError + Kd*rateError

#idk what this is above

vals = [] # list to save to csv
ts = [] # list to save to csv

# create encoder object on GPIO pins 17 and 18
encoder = RotaryEncoder(24, 25, max_steps=0)

# Define motor pins forward pin (in1) 22, backward (in2) 23, PWM (en) 24
in1 = 7
in2 = 8
en = 11


# initialize values
velCurr = 0
posCurr = 0
posLast = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()

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
	velCurr = ((posCurr-posLast)/(tcurr-tprev))/ppr # in rev/sec
	if(np.floor(tcurr/tdisp)-np.floor(tprev/tdisp))==1:
		print(velCurr , tcurr)
	tprev = tcurr
	posLast = posCurr
	# vals.append(np.abs(velCurr))
	# ts.append(tcurr)

# saveCSV = pd.DataFrame({'RevPSec': vals,
# 						'seconds': ts})

# saveCSV.to_csv('out.csv')
	
print('Done.')
GPIO.cleanup()
encoder.close()




