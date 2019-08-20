import RPi.GPIO as GPIO
from states import *
import time
import logging

MAX_ID=30
USER_ID_START=20
MOTOR_UP = 3
MOTOR_DOWN = 5
STOPPER_UP = 11
STOPPER_DOWN = 13
LED_RED=18
LED_GREEN=16
KEY=12

'''def saveRaw(f,a):
    print a
    raw_img = finger.GetImage()
    filename ='raw_img'+a+'.img'
    with open(filename, 'w') as file:
        file.write(raw_img) 
'''
def Enrollment(finger, id):             
    response = finger.EnrollStart(id)      
    if response[0]['ACK']:
    #####wait for FingerpressEnroll1
       waitforFinger(finger,states['Not_Pressed'])
       waitforFinger(finger,states['Pressed'])
    ######Captuer Finger_Enroll1      
       response = finger.CaptureFinger()   
       if response[0]['ACK']:        
    ########Enroll1
            response = finger.Enroll1(id)
            if response[0]['ACK']:ledNotification(states['ok'])
            else: return -1                                 
    #####Wait for Fingerpress Enroll2
       waitforFinger(finger,states['Not_Pressed'])
       waitforFinger(finger,states['Pressed'])       
     #####Capture Finger Enroll 2     
       response = finger.CaptureFinger()     
       if response[0]['ACK']:            
    #########Enroll2   
           response = finger.Enroll2(id)      
           if response[0]['ACK']:ledNotification(states['ok'])
           else: return -1               
    #####Wait for Fingerpress Enroll3   
       waitforFinger(finger,states['Not_Pressed'])
       waitforFinger(finger,states['Pressed'])
    ######Capture Finger Enroll3      
       response = finger.CaptureFinger() 
       if response[0]['ACK']:                  
    #######Enroll 3    
            response = finger.Enroll3(id)
            if response[0]['ACK']:ledNotification(states['ok'])
            else: return -1
    #####Wait for Fingerlift    
       waitforFinger(finger,states['Not_Pressed'])   
    ########Verify Enrollment   
       waitforFinger(finger,states['Pressed'])    
    ######Capture Finger Verification      
       response = finger.CaptureFinger() 
       if response[0]['ACK']:        
           response = finger.Verify(id)    
           if response[0]['ACK']:ledNotification(states['ok'])
           else:return -1
    
    else: return -1
    
    response = finger.GetEnrollCount()
    logging.info('EnrollCountNew: %d', response[0]['Parameter'])
    
def getfreeID(finger):
    response = finger.GetEnrollCount()
    print'EnrollCount:', response[0]['Parameter']
    if response[0]['Parameter'] > MAX_ID:return states['No_Space']
    else: 
        id = USER_ID_START                                 #ersten 20 Plaetze fuer Admin reserviert
        response = finger.CheckEnrolled(id)
        while response[0]['Parameter'] == 0 :
                id = id + 1
                response = finger.CheckEnrolled(id)
        return id  
         
def identifyFingerID(finger):
    response = finger.CaptureFinger()   
    if response[0]['ACK']:
        response = finger.Identify()
        if response[0]['ACK']:
            ledNotification(states['ok'])
            return response[0]['Parameter']         
        else : 
            ledNotification(states['not_ok'])
            return -1
    else: 
        ledNotification(states['not_ok'])
        return -1     
  
def waitforFinger(finger, state):
    if state == states['Pressed']:
        response = finger.IsPressFinger()
        while response[0]['Parameter'] != 0  :
            response = finger.IsPressFinger()
    elif state == states['Not_Pressed']:
        response = finger.IsPressFinger()   
        while response[0]['Parameter'] == 0  :
            response = finger.IsPressFinger()
       
def adminAction(finger,adminCommand):
    if adminCommand == adminCommands['AdminEnroll_NewUser'] :
       logging.info('New User')
       id = getfreeID(finger)
       if id !=states['No_Space']:
            err=Enrollment(finger,id)
            if err == -1:
                ledNotification(states['not_ok'])
       else:  
            logging.info('No Space left,consider changing the Max IDs')
            err=-1
       return err
    elif adminCommand == adminCommands['AdminDelete_All_Users']:
        logging.info('Delete all Users')
        for id in range (20,MAX_ID):
            finger.DeleteId(id)
        response = finger.GetEnrollCount()
        logging.info('EnrollCountNew: %d', response[0]['Parameter'])
        return 0
    elif adminCommand == adminCommands['AdminOpenBox']:
        finger.CmosLed()
        logging.info('Open Box')
        err=motor(actions['open'])
        while GPIO.input(KEY) !=1 :
                   #if ((time.clock()-waittime)>18): ledNotification(states['not_ok'])
                   pass
        err=motor(actions['close'])
        finger.CmosLed(True)
        return err
    elif adminCommand == adminCommands['AdminLogout'] :
       return -1

def getAdminCommand(id):    
    ''' id 1,11 New User
        id 2,12 Delete all Users
        id 3,13 Open Box
        id 0,10 Admin Logout
    '''
    if id == 1 or id == 11:return adminCommands['AdminEnroll_NewUser']
    elif id == 2 or id == 12 :return adminCommands['AdminDelete_All_Users']  
    elif id == 3 or id == 13 :return adminCommands['AdminOpenBox']
    elif id == 0 or id == 10 :return adminCommands['AdminLogout']
    else : return adminCommands['AdminLogout'] 
    
def setUserMode(id):
    if id == 0 or id ==10:return modes['Admin']
    elif id ==-1 or id < USER_ID_START:return modes['Default']
    else : return modes['User']
   
def blink(finger,state):  
    if state == states['ready']:blinkspeed(finger,modes['rapid'])
    elif state == states['ok']:blinkspeed(finger,modes['rapid'])
    elif state == states['not_ok']:blinkspeed(finger,modes['normal'])
               
def blinkspeed(finger,mode):        
        
    if mode == modes['normal']:
          for i in range(0,2):  
            finger.CmosLed(False)
            time.sleep(0.5)
            finger.CmosLed(True)
            time.sleep(1)
               
    elif mode == modes['rapid']:
          for i in range(0,2):
            finger.CmosLed(False)
            time.sleep(0.15)
            finger.CmosLed(True)
            time.sleep(0.25)        

def motor(action):
    if (GPIO.input(STOPPER_UP) ==1 and GPIO.input(STOPPER_DOWN) == 1) or (GPIO.input(STOPPER_UP) == 0 and GPIO.input(STOPPER_DOWN) == 0):
        return -1
    elif action == actions['open']:
        GPIO.output(MOTOR_DOWN,False)
        while GPIO.input(STOPPER_UP) != 1 :
            GPIO.output(MOTOR_UP,True)
        GPIO.output(MOTOR_UP,False)
    elif  action == actions['close']:
        GPIO.output(MOTOR_UP,False)
        while GPIO.input(STOPPER_DOWN) != 1 :
            GPIO.output(MOTOR_DOWN,True)
        GPIO.output(MOTOR_DOWN,False) 
    return checkMotorState()


def checkMotorState():
    if GPIO.input(STOPPER_UP) == 1 and GPIO.input(STOPPER_DOWN) == 0:
        return states['opened']
    elif GPIO.input(STOPPER_UP) == 0 and GPIO.input(STOPPER_DOWN) == 1:
        return states['closed']


def ledSwitch(led,on = False):   
    GPIO.output(led,on) 
    
def ledNotification(state):
    if state == states['ok']:
        for i in range(0,3):
            ledSwitch(LED_GREEN,True)
            time.sleep(0.15)
            ledSwitch(LED_GREEN)
            time.sleep(0.25)
    elif state == states['not_ok']:
        for i in range(0,2):
            ledSwitch(LED_RED)
            time.sleep(0.5)
            ledSwitch(LED_RED,True)
            time.sleep(1)     
