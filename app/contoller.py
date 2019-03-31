from app.sensors import TemperatureHumiditySensor, InputSensor
from app.alarm import Alarm
import json
from threading import Thread, ThreadError


class AlarmoController:
    """
    Class for controlling all functionality of Alarmo
    """
    def __init__(self):
        self.active_sensors = list()
        self.alarm_times = list()
        self.__load_configurations()
        self.alarm = Alarm(self.alarm_times)

    def run(self):
        """
        Run alarmo
        :return: None
        """
        alarm_display_thread = Thread(target=self.alarm.display)
        alarm_display_thread.setDaemon(True)
        alarm_display_thread.start()

        while True:
            pass

    def __load_configurations(self):
        """
        Loads JSON configs for alarm.
        :return: None, raises KeyError if config files are invalid
        """
        with open("./config/sensors.json") as sensor_json:
            sensor_config = json.load(sensor_json)

        if self.__validate_config(sensor_config, "sensors"):
            sensors_list = sensor_config["sensors"]
            for sensor in sensors_list:
                self.active_sensors.append(self.__create_sensor(sensor))
        else:
            raise KeyError("Error in sensors.json configuration, no 'sensors' key")

        with open("./config/alarm_times.json") as alarm_times_json:
            alarm_config = json.load(alarm_times_json)

        if self.__validate_config(alarm_config, "times"):
            alarm_list = alarm_config["times"]
            for alarm in alarm_list:
                self.alarm_times.append(alarm["alarm_time"])
        else:
            raise KeyError("Error in alarm_times.json configuration, no 'times' key")

    @staticmethod
    def __validate_config(config, config_type):
        """
        Validates a config file
        :param config: configuration dictionary
        :param config_type: config key
        :return: Boolean for valid config
        """
        return config_type in config and isinstance(config[config_type], list)

    @staticmethod
    def __create_sensor(sensor):
        """
        Creates sensor objects
        :param sensor: dictionary of sensor details
        :return: Sensor object
        """
        if sensor["type"] == "dht":
            sensor_object = TemperatureHumiditySensor(sensor["pin"])
            sensor_object.basic_return = False
        else:
            sensor_object = InputSensor(sensor["pin"], sensor["type"])
            sensor_object.basic_return = False
        return sensor_object