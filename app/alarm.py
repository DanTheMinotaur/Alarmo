from time import sleep
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime


class Alarm:
    def __init__(self):
        self.screen = self.__setup_screen()
        self.screen.clear()
        self.message = "Initilised"

    def display(self):
        while True:
            self.screen.message = "{time}\n{message}".format(
                time=datetime.now().strftime("%b-%d %H:%M:%S"),
                message=self.message
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
