from app.contoller import AlarmoController

alarm = AlarmoController()
try:
    alarm.run()
except KeyboardInterrupt:
    print("Closing Program")
    exit()