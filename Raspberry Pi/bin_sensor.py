import spidev
import time
import RPi.GPIO as GPIO
from libdw import pyrebase
from numpy import interp

from send_notif import bot_sendtext, getPrevStatus

url = 'https://bintheredonethatf04.firebaseio.com/'
apikey = 'AIzaSyCYDOcqRDhpQKMJcKPoczHyMVcYJogTFeU'

config = {
    'apiKey': apikey,
    'databaseURL': url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#setup for linking LED to GPIO pins 17 and 27
GPIO.setmode(GPIO.BCM)
LED1 = 17
LED2 = 27
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)


#setup for linking ultrasonic sensor to GPIO pin
TRIG1 = 23
ECHO1 = 24
TRIG2 = 13
ECHO2 = 19

GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

GPIO.output(TRIG1,0)
GPIO.output(TRIG2,0)

def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

#get previous status of the 2 bins
prev_bin1 = getPrevStatus("l1", "bin1")
prev_bin2 = getPrevStatus("l1", "bin2")

while True:
    # reading moisture sensor 1
    output1 = analogInput(0)
    output1 = interp(output1, [0, 1023], [100, 0])
    output1 = int(output1)
    print("Moisture 1:", output1)

    # reading ultrasonic sensor 1
    GPIO.output(TRIG1, GPIO.LOW)
    time.sleep(2) # give the sensor time to settle
    
    GPIO.output(TRIG1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG1, GPIO.LOW)
    
    while GPIO.input(ECHO1) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO1) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance1 = pulse_duration * 17150
    distance1 = round(distance1, 2)
    print("Distance 1: ", distance1, "cm")

    # update firebase and color of LED
    if output1 >= 10 and not 7 <= distance1 <= 9:
        GPIO.output(LED1, GPIO.HIGH)
        status1 = "full, spill"

    elif output1 >= 10 and 7 <= distance1 <= 9:
        GPIO.output(LED1, GPIO.HIGH)
        status1 = "not full, spill"

    elif output1 < 10 and not 7 <= distance1 <= 9:
        GPIO.output(LED1, GPIO.HIGH)
        status1 = "full, no spill"
    
    else:
        GPIO.output(LED1, GPIO.LOW)
        status1 = "not full, no spill"

    print(status1)
    db.child("l1").child("bin1").child("status").set(status1)

    # reading moisture sensor 2
    output2 = analogInput(1)
    output2 = interp(output2, [0, 1023], [100, 0])
    output2 = int(output2)
    print("Moisture 2:", output2)

    # reading ultrasonic sensors 1
    GPIO.output(TRIG2, GPIO.LOW)
    time.sleep(2) # give the sensor time to settle
    
    GPIO.output(TRIG2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG2, GPIO.LOW)
    
    while GPIO.input(ECHO2) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO2) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance2 = pulse_duration * 17150
    distance2 = round(distance2, 2)
    print("Distance 2: ", distance2, "cm")

    # update firebase and color of LED
    if output2 >= 10 and not 6.5 <= distance2 <= 9:
        GPIO.output(LED2, GPIO.HIGH)
        status2 = "full, spill"

    elif output2 >= 10 and 6.5 <= distance2 <= 9:
        GPIO.output(LED2, GPIO.HIGH)
        status2 = "not full, spill"

    elif output2 < 10 and not 6.5 <= distance2 <= 9:
        GPIO.output(LED2, GPIO.HIGH)
        status2 = "full, no spill"
    
    else:
        GPIO.output(LED2, GPIO.LOW)
        status2 = "not full, no spill"

    print(status2)
    db.child("l1").child("bin2").child("status").set(status2)
        
    time.sleep(1)

    
    if prev_bin1 == "not full, no spill" and status1 != "not full, no spill":
        bot_sendtext("Bin 1 at level 1 needs attention.\nPlease check your BinThereDoneThere App.")
    
    prev_bin1 = status1
        
    if prev_bin2 == "not full, no spill" and status2 != "not full, no spill":
        bot_sendtext("Bin 2 at level 1 needs attention.\nPlease check your BinThereDoneThere App.")
        
    prev_bin2 = status2
    
        
