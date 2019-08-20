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

def ledSwitch(led,on = False):   
    GPIO.output(led,on) 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_GREEN,GPIO.OUT)
GPIO.setup(LED_RED,GPIO.OUT)
ledSwitch(LED_GREEN)
ledSwitch(LED_RED)
ledSwitch(LED_GREEN, True)
time.sleep(1);
ledSwitch(LED_GREEN)

ledSwitch(LED_RED, True)
time.sleep(1);
ledSwitch(LED_RED)
GPIO.cleanup()