from app.sensors import TemperatureHumiditySensor, InputSensor
from app.weather import OpenWeather
from app.alarm import Alarm
from app.connect import AWSClient
import json
from threading import Thread, ThreadError
from time import sleep


class AlarmoController:
    """
    Class for controlling all functionality of Alarmo
    """
    def __init__(self):
        self.active_sensors = list()
        self.alarm_times = list()
        self.weather_connection = {}
        self.__load_configurations()
        self.__alarm = Alarm(self.alarm_times)
        self.aws_client = AWSClient(
            client_id="alarmo",
            host="a3p8hueujw0tur-ats.iot.eu-west-1.amazonaws.com",
            root_ca_path="./certs/AmazonRootCA1.crt",
            thing_cert_path="./certs/Alarmo.cert.pem",
            private_key_path="./certs/Alarmo.private.key"
        )
        self.aws_client.connect()


    def run(self):
        """
        Run alarmo
        :return: None
        """
        alarm_display_thread = Thread(target=self.__alarm.display)
        alarm_display_thread.setDaemon(True)
        alarm_display_thread.start()

        aws_read_command_thread = Thread(target=self.listen_for_readings)
        aws_read_command_thread.setDaemon(True)
        aws_read_command_thread.start()

        sensor_data_thread = Thread(target=self.publish_sensor_readings)
        sensor_data_thread.setDaemon(True)
        sensor_data_thread.start()

        while True:
            pass

    def override_alarm_message(self, message):
        self.__alarm.set_message(message)

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

        if self.__validate_config(sensor_config, "weather"):
            self.weather_connection["connection"] = OpenWeather(sensor_config["weather"]["key"])
            self.weather_connection["location"] = OpenWeather(sensor_config["weather"]["location"])

        with open("./config/alarm_times.json") as alarm_times_json:
            alarm_config = json.load(alarm_times_json)

        if self.__validate_config(alarm_config, "times"):
            alarm_list = alarm_config["times"]
            for alarm in alarm_list:
                self.alarm_times.append(alarm["alarm_time"])
        else:
            raise KeyError("Error in alarm_times.json configuration, no 'times' key")

    def listen_for_readings(self):
        command_topic = "Alarm/Command"
        while True:
            self.aws_client.receive(command_topic)
            if self.aws_client.new_message:
                self.__read_command(self.aws_client.get_message())


    def __read_command(self, command):
        print("Reading Command")
        if "message" in command:
            self.override_alarm_message(command["message"])
        if "time" in command:
            self.alarm_times.append(command["time"])
        print(command)

    def publish_sensor_readings(self, wait_time=1):
        """
        Sends sensor readings to AWS
        :param wait_time: time to wait before reading sensors again.
        :return:
        """
        while True:
            print(self.__read_sensors())
            sleep(wait_time)

    def __read_sensors(self):
        sensor_data = {}
        for sensor in self.active_sensors:
            sensor_data[sensor.sensor_type] = sensor.read()
        return sensor_data

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
