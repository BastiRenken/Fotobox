#!/usr/bin/python3
# Pakete importieren
import picamera
import os
import time
import RPi.GPIO as GPIO

# GPIO-Einstellungen
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Pin 4 als Eingang

# GPIO Outputs einstellen
gpio_outputs = [16, 12, 20, 21, 23, 25, 24, 18]
for pin in gpio_outputs:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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

# Kameraeinstellungen
camera = picamera.PiCamera()
camera.resolution = (3280, 2464)
camera.hflip = True
camera.vflip = True

zaehler = 1
while True:
    zeit = time.strftime("%y-%m-%d_%H-%M-%S")
    if GPIO.input(4) == GPIO.HIGH:
        zahl(fuenf, 1)
        zahl(vier, 1)
        for i in range(1, 5):
            zahl(drei, 1)
            zahl(zwei, 1)
            zahl(eins, 1)
            zahl_an(null)
            GPIO.output(18, GPIO.HIGH)
            camera.capture("media/%s_%d.jpg" %(zeit, i))
            GPIO.output(18, GPIO.LOW)
            zahl_aus(null)
            print("%d Bild %d aufgenommen!" %(zaehler, i))
        zaehler += 1
