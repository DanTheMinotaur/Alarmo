from time import sleep
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime
from app.sensors import Outputter


class Alarm:
    def __init__(self, alarm_times=None, last_message="", alarm_pin=10):
        self.screen = self.__setup_screen()
        self.screen.clear()
        self.__message = last_message
        self.alarm_times = sorted(list(alarm_times), reverse=True)
        self.alarm_buzzer = Outputter(alarm_pin)

    def set_message(self, message):
        self.screen.clear()
        self.__message = message

    def display(self):
        """
        Displays the current time and message set.
        :return:
        """
        self.set_message("Alarm @ {}".format(self.alarm_times[0]))
        alarm_countdown = 0
        started = False
        while True:
            current_time = datetime.now().strftime("%b-%d %H:%M")

            for time in self.alarm_times:
                if time in current_time:
                    self.set_message("WAKE UP!")
                    #self.alarm_buzzer.on()
                    if not started:
                        alarm_countdown = 10

            self.screen.message = "{time}\n{message}".format(
                time=current_time,
                message=self.__message
            )
            sleep(1)
            print(alarm_countdown)
            if alarm_countdown > 0:
                if not started:
                    started = True
                print("Lowering Countdown")
                alarm_countdown -= 1
            else:
                print("Alarm OFF")
                self.alarm_off()

    def alarm_off(self):
        self.alarm_buzzer.off()

    @staticmethod
    def __setup_screen():
        """
        Method creates screen
        :return: adafruit_character_lcd.character_lcd object
        """
        return characterlcd.Character_LCD_Mono(
            digitalio.DigitalInOut(board.D16),
            digitalio.DigitalInOut(board.D12),
            digitalio.DigitalInOut(board.D7),
            digitalio.DigitalInOut(board.D8),
            digitalio.DigitalInOut(board.D25),
            digitalio.DigitalInOut(board.D24),
            16,
            2
        )
