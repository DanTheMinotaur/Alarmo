import RPi.GPIO as GPIO


class InputSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)


class Tap(InputSensor):
    def __init__(self, pin):
        super(Tap, self).__init__(pin)

    def read(self):
        return bool(GPIO.input(self.pin))
