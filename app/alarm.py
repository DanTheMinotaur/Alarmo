from time import sleep
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime
from app.sensors import Outputter, InputSensor


class Alarm:
    """
    Class for controlling Alarm Clock Functionailty
    """
    def __init__(self, alarm_times=None, last_message="", alarm_pin=10, tap_pin=17):
        self.screen = self.__setup_screen()
        self.screen.clear()
        self.__message = last_message
        self.alarm_times = list(alarm_times)
        self.alarm_buzzer = Outputter(alarm_pin)
        self.alarm_tap = InputSensor(tap_pin, "Tap")

    def set_message(self, message):
        """
        Sets message for display
        :param message:
        :return:
        """
        self.screen.clear()
        self.__message = str(message)

    def display(self):
        """[0]
        Displays the current time and message set.
        :return: None
        """
        alarm_countdown = 0
        started = False
        tapped = False
        loop_count = 0
        while True:
            print(self.alarm_times)
            if len(self.alarm_times) > 0 and loop_count % 10 == 0:
                next_time = sorted(self.alarm_times, reverse=True)[0]
                self.set_message("Alarm @ {}".format(next_time))

            if loop_count % 20:
                self.set_message(self.__message)

            current_time = datetime.now().strftime("%b-%d %H:%M")

            if started:
                tapped = self.alarm_tap.read()
                print("Tapped: " + str(tapped))

            for time in self.alarm_times:
                if time in current_time:
                    self.set_message("WAKE UP!")
                    #self.alarm_buzzer.on()
                    if not started:
                        alarm_countdown = 30

            self.screen.message = "{time}\n{message}".format(
                time=current_time,
                message=self.__message
            )
            sleep(1)
            print(alarm_countdown)

            if alarm_countdown > 0:
                if tapped:
                    alarm_countdown = 1
                    self.snooze_mode()
                if not started:
                    started = True
                tapped = False
                alarm_countdown -= 1
            else:
                self.alarm_off()

            loop_count += 1

    def snooze_mode(self):
        """
        Applies Snooze Functionality
        :return:
        """
        print("Entering Snooze Mode") # TODO add Movement Function


    def alarm_off(self):
        """
        Exposes Alarm off to external program
        :return:
        """
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
