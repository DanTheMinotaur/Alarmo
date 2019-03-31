from time import sleep
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime


class Alarm:
    def __init__(self, alarm_times=None, last_message=""):
        self.screen = self.__setup_screen()
        self.screen.clear()
        self.__message = last_message
        self.alarm_times = sorted(list(alarm_times), reverse=True)

    def set_message(self, message):
        self.screen.clear()
        self.__message = message

    def display(self):
        """
        Displays the current time and message set.
        :return:
        """
        self.set_message("Alarm @ {}".format(self.alarm_times[0]))
        while True:
            current_time = datetime.now().strftime("%b-%d %H:%M:%S")

            for time in self.alarm_times:
                if time in current_time:
                    self.set_message("WAKE UP!")

            self.screen.message = "{time}\n{message}".format(
                time=current_time,
                message=self.__message
            )
            sleep(1)

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
