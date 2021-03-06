#!/usr/bin/python3
# Pakete importieren
import picamera
import os
import time
import RPi.GPIO as GPIO

# Ausgabe aktivieren/deaktivieren
ausgabe = 0

# GPIO-Einstellungen
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO Out- und Inputs einstellen
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Pin 4 als Eingang
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Pin 5 als Eingang
gpio_outputs = [16, 12, 20, 21, 23, 25, 24]
for pin in gpio_outputs:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)

# Variablen für LCD definieren
null = [16, 12, 20, 23, 25, 24]
eins = [12, 23]
zwei = [16, 12, 21, 25, 24]
drei = [16, 12, 21, 23, 24]
vier = [20, 12, 21, 23]
fuenf = [16, 20, 21, 24, 23]
sechs = [16, 20, 21, 25, 24, 23]
sieben = [16, 12, 23]
acht = [16, 12, 20, 21, 23, 25, 24]
neun = [16, 12, 20, 21, 23, 24]

# Funktionen für LCD definieren
def zahl(ziffer, dauer):
    for pin in ziffer:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(dauer)
    for pin in ziffer:
        GPIO.output(pin, GPIO.LOW)
def zahl_an(ziffer):
    for pin in ziffer:
        GPIO.output(pin, GPIO.HIGH)
def zahl_aus(ziffer):
    for pin in ziffer:
        GPIO.output(pin, GPIO.LOW)

livestream = "nohup raspistill -v -hf --fullscreen -t 0 > /dev/null 2>&1 &"

os.system(livestream)
os.system("/opt/vc/bin/tvservice -p")
zaehler = 1
while True:
    sperre = 0
    if GPIO.input(4) == GPIO.HIGH:
        zeit = time.strftime("%y-%m-%d_%H-%M-%S")
        zahl(fuenf, 1)
        zahl(vier, 1)
        zahl(drei, 1)
        for i in range(1, 4):
            zahl(zwei, 1)
            zahl(eins, 1)
            zahl_an(null)
            os.system("sudo pkill raspistill") #Bild ausblenden
            camera = picamera.PiCamera()
            camera.resolution = (3280, 2464)
            GPIO.output(18, GPIO.LOW) #Fotolicht an
            camera.capture("/home/pi/Desktop/Fotobox/media/%s_%d.jpg" %(zeit, i)) #Bild aufnehmen
            GPIO.output(18, GPIO.HIGH) #Fotolicht aus
            camera.close()
            os.system(livestream) #Bild einblenden
            zahl_aus(null)
            if ausgabe == 1:
                print("Serie %d Bild %d %s" %(zaehler, i, zeit)) #Terminalausgabe
        zaehler += 1
    elif GPIO.input(5) == GPIO.HIGH:
        os.system("sudo pkill raspistill") #Bild ausblenden
        time.sleep(1)
        while sperre == 0:
            if GPIO.input(5) == GPIO.HIGH:
                os.system(livestream)
                time.sleep(1)
                sperre = 1
            elif GPIO.input(4) == GPIO.HIGH: #System herunterfahren
                os.system("sudo shutdown 0")
