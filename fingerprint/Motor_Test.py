import RPi.GPIO as GPIO
import time
from states import *

MOTOR_UP = 3
MOTOR_DOWN = 5
STOPPER_UP = 11
STOPPER_DOWN = 13
#GPIO INIT#########

print 'GPIO Init'
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_UP,GPIO.OUT)
GPIO.setup(MOTOR_DOWN,GPIO.OUT)
GPIO.output(MOTOR_UP,False)
GPIO.output(MOTOR_DOWN,False)
GPIO.setup(STOPPER_UP,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(STOPPER_DOWN,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

def motor(action):
    #if (GPIO.input(STOPPER_UP) ==1 and GPIO.input(STOPPER_DOWN) == 1) or (GPIO.input(STOPPER_UP) == 0 and GPIO.input(STOPPER_DOWN) == 0):
        
     #   return -1
    if action == actions['open']:
        GPIO.output(MOTOR_DOWN,False)
        while GPIO.input(STOPPER_UP) != 1 :
            GPIO.output(MOTOR_UP,True)
        GPIO.output(MOTOR_UP,False)
    
    elif  action == actions['close']:
        GPIO.output(MOTOR_UP,False)
        while GPIO.input(STOPPER_DOWN) != 1 :
            GPIO.output(MOTOR_DOWN,True)
        GPIO.output(MOTOR_DOWN,False) 

err=motor(actions['open'])
if err == -1:
    print 'Fehler'
    
time.sleep(5)
err=motor(actions['close'])
if err == -1:
    print 'Fehler'
       

GPIO.cleanup()


