import RPi.GPIO as GPIO


class InputSensor:
    def __init__(self, pin, sensor_type="Input", basic_return=True):
        try:
            self.pin = int(pin)
            self.sensor_type = str(sensor_type)
            self.basic_return = bool(basic_return)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
        except ValueError:
            print("Invalid Setup Type")

    def read(self):
        sensor_value = GPIO.input(self.pin)
        if self.basic_return:
            return bool(sensor_value)
        else:
            return {
                "sensor_type": self.sensor_type,
                "value": sensor_value,
                "pin": self.pin
            }
