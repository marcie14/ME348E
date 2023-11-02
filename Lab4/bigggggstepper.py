import serial
import time
from time import sleep
import numpy as np
import RPi.GPIO as GPIO
import asyncio
import sys

motorchannel = (9,11,7,6)

i = 0
pos = 0
neg = 0
y = 0
delay = 0.03

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorchannel,GPIO.out)

try:
    while(1):
        GPIO.output(9,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(7,GPIO.LOW)
        GPIO.output(6,GPIO.LOW)
        x = input()
        if x>0 and x<=400:
            for y in range(x,0,-1):
                if neg == 1:
                    if i ==7:
                        i=0
                    else:
                        i=i+1
                    y=y+2
                    neg=0
                pos=1
                if i==0:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==1:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)
                
                elif i==2:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==3:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==4:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==5:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)

                elif i==6:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)

                elif i==7:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)
                if i==7:
                    i=0
                    continue
                i=i+1
        elif x<0 and x>=400:
            x=x*-1
            for y in range(x,0,-1):
                if pos==1:
                    if i==0:
                        i=7
                    else:
                        i=i-1
                    y=y+3
                    pos=0
                neg=1
                if i==0:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==1:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)
                
                elif i==2:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==3:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.HIGH)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==4:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.LOW)
                    time.sleep(delay)

                elif i==5:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.HIGH)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)

                elif i==6:
                    GPIO.output(9,GPIO.LOW)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)

                elif i==7:
                    GPIO.output(9,GPIO.HIGH)
                    GPIO.output(11,GPIO.LOW)
                    GPIO.output(7,GPIO.LOW)
                    GPIO.output(6,GPIO.HIGH)
                    time.sleep(delay)
                if i==0:
                    i=7
                    continue
                i=i-1
except KeyboardInterrupt:
    GPIO.cleanup()
    
