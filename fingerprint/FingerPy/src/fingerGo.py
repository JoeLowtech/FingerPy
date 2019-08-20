import fingerpi as fp
import fingerfunc as ff
import time
import RPi.GPIO as GPIO
import logging
from states import *

'''TODO
Name programm aendern
'''
####Logging Config
logging.basicConfig(level=logging.DEBUG, filename="logfileFinger", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    
MOTOR_UP = 3
MOTOR_DOWN = 5
STOPPER_UP = 11
STOPPER_DOWN = 13
LED_RED=18
LED_GREEN=16
KEY=12

def userMode(finger,mode):
   finger.CmosLed()
   if ff.checkMotorState() == states['closed']:
           logging.info('Motor auf')
           err=ff.motor(actions['open'])
           if err == -1:
               ff.ledNotification(states['not_ok'])
           else:    
               ff.ledSwitch(LED_RED)
               ff.ledSwitch(LED_GREEN,True)
               waittime=time.clock()
               while GPIO.input(KEY) !=1 and (time.clock() - waittime) < 300:
                   #if ((time.clock()-waittime)>18): ff.ledNotification(states['not_ok'])
                   pass        
               ff.ledSwitch(LED_RED,True)
               ff.ledSwitch(LED_GREEN)  
   if ff.checkMotorState() == states['opened']:
           logging.info('Motor schliessen')
           err=ff.motor(actions['close'])
           if err == -1:
               ff.ledNotification(states['not_ok'])
   logging.info('UserLogout')
   finger.CmosLed(True)
    
def adminMode(finger,mode):
    ff.ledSwitch(LED_GREEN, True)
    while mode == modes['Admin']:
        ff.waitforFinger(finger,states['Not_Pressed'])
        ff.waitforFinger(finger,states['Pressed'])
        err=ff.adminAction(finger,ff.getAdminCommand(ff.identifyFingerID(finger)))
        if err == -1:
            mode = modes['Default']
            logging.info('AdminLogout')
            ff.ledSwitch(LED_GREEN)

#===============================================================================
logging.info('GPIO Init')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_UP,GPIO.OUT)
GPIO.setup(MOTOR_DOWN,GPIO.OUT)
GPIO.setup(LED_GREEN,GPIO.OUT)
GPIO.setup(LED_RED,GPIO.OUT)
GPIO.setup(KEY,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(STOPPER_UP,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(STOPPER_DOWN,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
#===============================================================================
ff.ledSwitch(LED_GREEN)
ff.ledSwitch(LED_RED,True)
GPIO.output(MOTOR_UP,False)
GPIO.output(MOTOR_DOWN,False)
if ff.checkMotorState() ==states['opened']:
    err=ff.motor(actions['close'])
    if err == -1:
        ff.ledNotification(states['not_ok'])
#===============================================================================
logging.info('Fingerprint Sensor Init')
finger = fp.FingerPi()
finger.Open(extra_info = True, check_baudrate = True)
finger.ChangeBaudrate(115200)
finger.CmosLed()
logging.info('ready')
#===============================================================================

#=========================SetAdmin_one==========================================
# logging.info('SetAdminMode')
#  
# logging.info('erster Admin')
# finger.DeleteId(0)
# ff.Enrollment(finger,0)
#  
# logging.info('AdminCommand adminEnroll_NewUser')
# finger.DeleteId(1)
# ff.Enrollment(finger,1)
#  
# logging.info('AdminCommand adminDetele_All_Users')
# finger.DeleteId(2)
# ff.Enrollment(finger,2)
#  
# logging.info('AdminCommand adminOpenBox')
# finger.DeleteId(3)
# ff.Enrollment(finger,3)
#===============================================================================

#===============================================================================
# #SetAdmin_two
# #logging.info('zweiter Admin')
# #finger.DeleteId(1)
# #ff.Enrollment(finger,10)
#===============================================================================

#===============================================================================
# logging.info('Delete all')
# finger.DeleteAll()
# response = finger.GetEnrollCount()
# logging.info('EnrollCountNew: %d', response[0]['Parameter'])
#===============================================================================

#==========================NormalMode===========================================
while(1):
    if GPIO.input(KEY) ==1:
        finger.CmosLed(True)
        logging.info('NormalMode')
        ff.waitforFinger(finger,states['Not_Pressed'])
        ff.waitforFinger(finger,states['Pressed'])
        mode = ff.setUserMode(ff.identifyFingerID(finger))
        if mode == modes['Admin']:
            logging.info('Adminmodus')
            adminMode(finger,mode)
        elif mode == modes['User']:
            logging.info('Usermodus')
            ff.ledNotification(states['ok'])
            userMode(finger,mode)
        else: 
            logging.info('Defaultmodus')
            ff.ledNotification(states['not_ok'])
        finger.CmosLed()       
#===============================================================================
logging.info('Close Connection')
finger.CmosLed(False)
finger.Close()
GPIO.cleanup()
