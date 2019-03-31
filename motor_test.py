import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

print("Going forwards")
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.HIGH)

sleep(2)

print("Going backwards")
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.HIGH)
GPIO.output(Motor1E, GPIO.HIGH)

sleep(2)

sleep(2)

print("Stopping motor")
GPIO.output(Motor1E, GPIO.LOW)

GPIO.cleanup()
