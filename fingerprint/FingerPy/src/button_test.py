import fingerpi as fp
import fingerfunc as ff
import time
import RPi.GPIO as GPIO
import logging
from states import *

MOTOR_UP = 3
MOTOR_DOWN = 5
STOPPER_UP = 11
STOPPER_DOWN = 13
LED_RED=18
LED_GREEN=16
KEY=12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(KEY,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(STOPPER_UP,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(STOPPER_DOWN,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

while GPIO.input(KEY) !=1:
    print "Drueck Gruen\n"
    
while GPIO.input(STOPPER_UP) !=1:
    print "Drueck oben\n"
    
while GPIO.input(STOPPER_DOWN) !=1:
    print "Drueck unten\n"
    
print "alles ok\n"
    

GPIO.cleanup()