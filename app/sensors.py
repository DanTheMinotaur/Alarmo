import RPi.GPIO as GPIO
import Adafruit_DHT
import time


class Sensor:
    def __init__(self, pin, sensor_type="Input", basic_return=True):
        self.pin = pin
        self.sensor_type = str(sensor_type)
        self.basic_return = bool(basic_return)
        self.value = None

    def format_readings(self):
        if self.basic_return:
            if isinstance(self.value, dict):
                return self.value
            else:
                return bool(self.value)
        else:
            return {
                "sensor_type": self.sensor_type,
                "value": self.value,
                "pin": self.pin,
                "time": time.time()
            }


class Outputter:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


class TemperatureHumiditySensor(Sensor):
    DHT_TYPE = Adafruit_DHT.DHT11

    def __init__(self, pin):
        super(TemperatureHumiditySensor, self).__init__(pin=pin)
        self.sensor_type = "Temperature and Humidity"

    def read(self):
        while True:
            humidity, temperature = Adafruit_DHT.read(self.DHT_TYPE, self.pin)
            if humidity is not None and temperature is not None:
                self.value = {
                    "temperature": temperature,
                    "humidity": humidity
                }
                return self.format_readings()
            else:
                continue


class InputSensor(Sensor):
    """
    Class for creating input sensor objects
    """
    def __init__(self, pin, sensor_type="Input"):
        super(InputSensor, self).__init__(pin, sensor_type)
        """
        :param pin: The pin number for the input device
        :param sensor_type: The name of the sensor being created
        :param basic_return: Return Type of data being read
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)


    def read(self):
        """
        Reads data from input sensor
        :return: Returns boolean value if basic_return is set to True, or a dictionary with object information.
        """
        self.value = GPIO.input(self.pin)
        return self.format_readings()
