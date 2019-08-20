states = {
    'Not_Pressed' : 0x01, #Finger auf dem Sensor soll weg
    'Pressed' :     0x02, #Finger soll auf den Sensor
    'No_Space':     0xFF, #Kein Speicherplatz mehr frei    
        
    'ready':    0x10, #Blink Geraet bereit,nicht benoetigt
    'ok'   :    0x11, #Blink Operation erfolgreich ausgefuehrt
    'not_ok':   0x12, #Blink Opertaion nicht erfoglreich  
    'opened':   0x20, #Box offen
    'closed':   0x21, #Box geschlossen
    'MotorError': 0x22 #nicht benoetigt
    }


modes = {
    'Admin' :   0xF0, #Adminmodus
    'User'  :   0xE0, #User 
    'Default' : 0xD0, #Default
    
    'normal' : 0x01, #Led blinkt mit 0.5s 3 mal
    'rapid' :  0x02 #Led blinkt mit 0.2s 3 mal
    }

actions = {
    'open'  : 0x01, #Motorbefehl
    'close' : 0x02  #Motorbefehl
    }

adminCommands = {
    'AdminEnroll_NewUser': 0xF1, #Neuen User einspeichern 
    'AdminDelete_All_Users' :0xF2, #Admin loescht alle Fingerabdruecke ausser die des Admins
    'AdminOpenBox': 0xF3, #Deckel oeffnen und schliessen
    'AdminLogout':0xF9 
    }