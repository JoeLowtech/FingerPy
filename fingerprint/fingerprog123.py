import fingerpi as fp
import fingerfunc as ff
import time
import RPi.GPIO as GPIO

#GPIO INIT#########

print 'GPIO Init'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)


#Fingerprint INIT########
print 'Fingerprint Sensor Init'

f = fp.FingerPi()
f.Open(extra_info = True, check_baudrate = True)
f.ChangeBaudrate(115200)

print 'ready'

# nur vorlaeufig simuliert Deckel
while (ff.topCheck() == False):()

print "Zu" 
while True:  
    
    if ff.activateButton() and ff.topCheck():  
        n=1
        while n!= 10:
            f.CmosLed(False)
            time.sleep(1)
            f.CmosLed(True)
            time.sleep(1)
            n=n+1
     
    f.CmosLed(False)       



f.Close()

GPIO.cleanup()