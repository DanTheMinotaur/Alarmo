from app.sensors import InputSensor
from time import sleep

pin = int(input("Enter the pin for testing: "))
sensor_type = str(input("What Type of Sensor are you testing"))

sensor = InputSensor(pin, sensor_type, False)

while True:
    sensor_data = sensor.read()
    if sensor_data["value"]:
        print("{} Detected".format(sensor_data["sensor_type"]))
    else:
        print("Nothing Detected")
    sleep(0.1)
