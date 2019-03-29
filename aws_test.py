from app.connect import AWSClient
from time import sleep
import random


def generate_random_data():
    return [
        {
            "sensor_type": "Motion",
            "value": bool(random.getrandbits(1)),
            "pin": random.randint(1, 26)
        },
        {
            "sensor_type": "Light",
            "value": bool(random.getrandbits(1)),
            "pin": random.randint(1, 26)
        },
        {
            "sensor_type": "Weather",
            "value": {
                "Temperature": round(random.uniform(1.5, 40.0), 2),
                "Humidity": round(random.uniform(1.5, 40.0), 2)
            },
            "pin": random.randint(1, 26)
        }
    ]

client = AWSClient(
    client_id="RaspPISender",
    host="a17mh16tz1p39u-ats.iot.eu-west-1.amazonaws.com",
    root_ca_path="./certs/root-CA.crt",
    thing_cert_path="./certs/PIThingCA.cert.pem",
    private_key_path="./certs/PIThingCA.private.key"
)
client.connect()

sleep_time = 10

while True:
    sample_data = generate_random_data()
    print("Random data to send: " + str(sample_data))
    client.send(sample_data, "alarm/test")
    print("Sleeping for {} seconds".format(sleep_time))
    sleep(sleep_time)
