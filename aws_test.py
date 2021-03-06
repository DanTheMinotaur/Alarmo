from app.connect import AWSClient
from time import sleep
import random
import time

def generate_random_data():
    object_list = [
        {
            "sensor_type": "Motion",
            "value": bool(random.getrandbits(1)),
            #"pin": random.randint(1, 26),
            "time": time.time()
        },
        {
            "sensor_type": "Light",
            "value": bool(random.getrandbits(1)),
            #"pin": random.randint(1, 26),
            "time": time.time()
        },
        {
            "sensor_type": "Weather",
            "value": {
                "Temperature": round(random.uniform(1.5, 40.0), 2),
                "Humidity": round(random.uniform(1.5, 40.0), 2)
            },
            #"pin": random.randint(1, 26),
            "time": time.time()
        }
    ]
    return object_list[random.randint(0, len(object_list) - 1)]

client = AWSClient(
    client_id="alarmo",
    host="a3p8hueujw0tur-ats.iot.eu-west-1.amazonaws.com",
    root_ca_path="./certs/AmazonRootCA1.crt",
    thing_cert_path="./certs/Alarmo.cert.pem",
    private_key_path="./certs/Alarmo.private.key"
)
client.connect()

sleep_time = 10

while True:
    sample_data = generate_random_data()
    print("Random data to send: " + str(sample_data))
    client.send(sample_data, "sdk/test/Python")
    print("Sleeping for {} seconds".format(sleep_time))
    sleep(sleep_time)
