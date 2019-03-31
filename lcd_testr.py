import Adafruit_CharLCD as LCD
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime

lcd_rs = digitalio.DigitalInOut(board.D16)
lcd_en = digitalio.DigitalInOut(board.D12)
lcd_d7 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D8)
lcd_d4 = digitalio.DigitalInOut(board.D7)
lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.clear()
lcd.color = [0, 100, 0]

# https://learn.adafruit.com/character-lcds/python-circuitpython
while True:
    lcd.message = "Hello\n{}".format(datetime.now().strftime("%b-%d %H:%M:%S"))
    time.sleep(1)
#
# rs = 17
# en = 12
# d4 = 7
# d5 = 8
# d6 = 25
# d7 = 24
# lcd_backlight = 4
# lcd_columns = 16
# lcd_rows = 2
#
# lcd = LCD.Adafruit_CharLCD(rs, en, d4, d5, d6, d7, lcd_columns, lcd_rows, lcd_backlight)
#
# lcd.message('Hello\nworld!')
# # Wait 5 seconds
#
# time.sleep(5.0)
# lcd.clear()
# text = input("Type Something to be displayed: ")
# lcd.message(text)
#
# # Wait 5 seconds
# time.sleep(5.0)
# lcd.clear()
# lcd.message('Goodbye\nWorld!')
#
# time.sleep(5.0)
# lcd.clear()