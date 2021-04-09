"""
Зарегистрироваться на https://openweathermap.org/api
и написать функцию, которая получает погоду в данный
момент для города, название которого получается через
input. https://openweathermap.org/current
"""
import requests
from pprint import pprint


def get_weather(key, city):
    get_url = 'https://api.openweathermap.org/data/2.5/weather?'
    current_weather = requests.get(get_url, params={'q': city, 'appid': key})
    data = current_weather.json()
    return data


pprint(get_weather('', input('enter city name: ')))
