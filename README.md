# Alarmo
IoT Alarm Clock
===============

The goal of the project was to build an IoT alarm clock which functions as a
normal alarm clock but when not in use transmit sensor data regarding the room
the alarm is in and store it in an offsite database.

![Alarmo Picture](https://github.com/DanTheMinotaur/Alarmo/blob/fca78d1d51100c9fedd71aa2bf4e692209114859/Alarmo.jpg?raw=true)

Features
========

-   Displays Current Time and Date

-   Shows periodic weather data on the lower part of the screen.

-   Detects Motion, Sound, Light, Temperature, Humidity.

-   Snooze mode via tilt/tap of the device.

-   Multithreaded Application (Sensor data, Transmitting to AWS, Display,
    Collect Weather Data running on separate threads)

-   Makes noise once the alarm has been triggered.

-   Can move as snooze mode, via legs.

-   Stores Data from sensors in AWS Dynamo DB (NoSQL)

-   Alarms Controlled via Android App

-   The user can set a display message via android app.

-   The user can change the rate at which sensor data is sent to AWS via App.

-   Uses MQTT Protocol for communication via AWS as a broker.
