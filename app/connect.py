from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
from datetime import datetime
from time import sleep
import logging

class AWSClient:
    """
    Class is used to connect to AWS IoT service and provides methods for sending and recieving data from AWS IoT
    platform
    """

    def __init__(self, client_id, host, root_ca_path, thing_cert_path, private_key_path, port=8883):
        self.logger = logging.basicConfig(
            filename=datetime.now().strftime("./log/pi-%Y-%m-%d.log"),
            level=logging.ERROR,
            format='%(asctime)s %(levelname)-10s %(name)s %(message)s',
        )
        self.client_id = client_id
        self.aws_client = AWSIoTMQTTClient(client_id)
        self.aws_client.configureEndpoint(host, port)
        self.aws_client.configureCredentials(root_ca_path, private_key_path, thing_cert_path)
        self.aws_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.aws_client.configureOfflinePublishQueueing(-1)
        self.aws_client.configureDrainingFrequency(2)
        self.aws_client.configureConnectDisconnectTimeout(10)
        self.aws_client.configureMQTTOperationTimeout(5)

        self.__latest_message = None
        self.new_message = False

        print("AWS Config Set")

    def connect(self):
        """
        Connects AWS IoT Client and sleeps to allow connection to established
        :return: None
        """
        self.aws_client.connect()
        sleep(2)
        print("Client %s Connected" % self.client_id)

    def send(self, data, topic="IoTMessage"):
        """
        Sends data to IoT broker with chosen topic and data payload
        :param data: Json/Dictionary of data to be transmitted.
        :param topic: The desited MTQQ topic for data to be posted to
        :return: None
        """
        data_message = dict(data)

        if data_message:
            data_message["thing_time"] = str(datetime.now())

            json_message = json.dumps(data_message)
            self.aws_client.publish(topic, json_message, 1)
            print("Sent %s message: %s " % (topic, json_message))

    def receive(self, topic="IoTMessage"):
        """
        Subscripbes to a particualr topic set and sends payload to call back method.
        :param topic:
        :return:
        """
        self.aws_client.subscribe(topic, 1, self.__call_back)

    def __call_back(self, client, user_data, message):
        """
        Callback for MQTT Client when it receives a message
        :param client: client id UNUSED
        :param user_data: user data UNSUED
        :param message: data that is recieved from broker
        :return:
        """
        try:
            self.__latest_message = json.loads(message.payload.decode('utf-8'))
            self.new_message = True
        except ValueError:
            error_text = "Malformed JSON Data: " + str(message.payload.decode('utf-8'))
            print(error_text)
            logging.error(error_text)

    def get_message(self):
        """
        Method for getting a new message sets new message to false to avoid duplication of messages.
        :return: dict or string of message
        """
        self.new_message = False
        return self.__latest_message

    def disconnect(self):
        """ Disconnects the AWS client """
        self.aws_client.disconnect()
        print("Client %s Disconnected" % self.client_id)
