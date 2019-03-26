from app.sensors import InputSensor, TemperatureHumiditySensor
from time import sleep
import json

print("Starting Test")
loop_time = None
sensors = list()

with open("config/sensors.json") as json_file:
    sensor_config = json.load(json_file)
    print(sensor_config)
    if "tests" in sensor_config:
        if "loop_time" in sensor_config["tests"]:
            loop_time = sensor_config["tests"]["loop_time"]

    if loop_time is None:
        loop_time = 0.1

    if "sensors" in sensor_config and isinstance(sensor_config["sensors"], list):
        for sensor in sensor_config["sensors"]:
            if sensor["type"] == "Weather":
                obj = TemperatureHumiditySensor(sensor["pin"])
                obj.basic_return = False
                sensors.append(obj)
            else:
                obj = InputSensor(sensor["pin"], sensor["type"])
                obj.basic_return = False
                sensors.append(obj)

while True:
    for sensor in sensors:
        sensor_data = sensor.read()
        print(sensor_data)
        if sensor_data["value"]:
            print("{} Detected".format(sensor_data["sensor_type"]))
        else:
            print("{} Nothing Detected".format(sensor_data["sensor_type"]))
    sleep(loop_time)
