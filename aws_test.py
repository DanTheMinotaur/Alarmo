from app.connect import AWSClient

client = AWSClient(
    client_id="RaspPISender",
    host="a17mh16tz1p39u-ats.iot.eu-west-1.amazonaws.com",
    root_ca_path="./certs/root-CA.crt",
    thing_cert_path="./certs/PIThingCA.cert.pem",
    private_key_path="./certs/PIThingCA.private.key"
)
client.connect()

client.send({"Hello": "World"})