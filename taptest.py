from app.sensors import Tap
from time import sleep

tap = Tap(21)

while True:
    if tap.read():
        print("Tap Detected")
    else:
        print("Nothing Detected")
    sleep(0.1)
