from app.sensors import InputSensor, TemperatureHumiditySensor
from time import sleep
import json
import argparse
import RPi.GPIO as GPIO

parser = argparse.ArgumentParser(description="Test Alarmo Sensors")
parser.add_argument("--sensor", "-s", help="Choose a sensor type to test")
parser.add_argument("--time", "-t", help="Choose a time to wait to read sensor from")

args = parser.parse_args()

print("Starting Test")
loop_time = None
sensors = list()

def create_sensor(sensor):
    if sensor["type"] == "dht":
        object = TemperatureHumiditySensor(sensor["pin"])
        object.basic_return = False
    else:
        object = InputSensor(sensor["pin"], sensor["type"])
        object.basic_return = False
    return object

with open("config/sensors.json") as json_file:
    sensor_config = json.load(json_file)
    print(sensor_config)
    if "tests" in sensor_config:
        if "loop_time" in sensor_config["tests"]:
            loop_time = sensor_config["tests"]["loop_time"]

    if loop_time is None:
        loop_time = 1

    if args.time:
        loop_time = float(args.time)

    if "sensors" in sensor_config and isinstance(sensor_config["sensors"], list):
        if args.sensor is None: # Create all sensors
            for sensor in sensor_config["sensors"]:
                sensors.append(create_sensor(sensor))
        else:
            for sensor in sensor_config["sensors"]:
                print(sensor)
                if args.sensor in sensor["type"]:
                    sensors.append(create_sensor(sensor))

if len(sensors) == 0:
    raise Exception("Invalid Sensor Value not found in Sensor Config File -s={}".format(args.sensor))

try:
    while True:

            for sensor in sensors:
                sensor_data = sensor.read()
                print(sensor_data)
                if sensor_data["value"]:
                    print("{} Detected".format(sensor_data["sensor_type"]))
                else:
                    print("{} Nothing Detected".format(sensor_data["sensor_type"]))
            sleep(loop_time)
except KeyboardInterrupt:
    print("User Closed Testing Program")
finally:
    GPIO.cleanup()
