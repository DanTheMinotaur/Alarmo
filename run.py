from app.contoller import AlarmoController

# Runs application

alarm = AlarmoController()
try:
    alarm.run()
except KeyboardInterrupt:
    print("Closing Program")
    exit()