import requests


class OpenWeather:
    def __init__(self, api_key):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?APPID={}".format(api_key)

    def get_weather_by_city(self, city):
        return requests.get(self.base_url + "&q={}".format(city)).json()

#
# test = OpenWeather("9c5881376dd9a6d8655bdb7467a25770")
#
# print(test.get_weather_by_city("Dublin"))