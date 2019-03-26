import RPi.GPIO as GPIO


class InputSensor:
    """
    Class for creating input sensor objects
    """
    def __init__(self, pin, sensor_type="Input", basic_return=True):
        """
        :param pin: The pin number for the input device
        :param sensor_type: The name of the sensor being created
        :param basic_return: Return Type of data being read
        """
        try:
            self.pin = int(pin)
            self.sensor_type = str(sensor_type)
            self.basic_return = bool(basic_return)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.IN)
        except ValueError:
            print("Invalid Setup Type")

    def read(self):
        """
        Reads data from input sensor
        :return: Returns boolean value if basic_return is set to True, or a dictionary with object information.
        """
        sensor_value = GPIO.input(self.pin)
        if self.basic_return:
            return bool(sensor_value)
        else:
            return {
                "sensor_type": self.sensor_type,
                "value": sensor_value,
                "pin": self.pin
            }
