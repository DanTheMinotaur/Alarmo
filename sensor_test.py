from app.sensors import InputSensor, WeatherHumiditySensor
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
                sensors.append(
                    WeatherHumiditySensor(sensor["pin"])
                )
            else:
                sensors.append(
                    InputSensor(sensor["pin"], sensor["type"], False)
                )

while True:
    for sensor in sensors:
        sensor_data = sensor.read()

        if isinstance(sensor_data["value"], dict):
            print(sensor_data["value"])
            break
        
        if sensor_data["value"]:
            print("{} Detected".format(sensor_data["sensor_type"]))
        else:
            print("{} Nothing Detected".format(sensor_data["sensor_type"]))
    sleep(loop_time)
