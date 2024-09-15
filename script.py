"""
To be completed when free
To implement weather api to get weather condiitons
To implement task scheduler or add in startup
"""

import requests
import json
import os
from datetime import datetime, timedelta

# Replace with your OpenWeatherMap API key and city details
API_KEY = 'your_openweathermap_api_key'
CITY = 'your_city'
COUNTRY = 'your_country_code'

# File to store the last rain date
FILE_PATH = os.path.expanduser('~\\last_rain_check.json')

def get_weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def has_rained_recently():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
            last_rain_date = datetime.strptime(data['last_rain_date'], '%Y-%m-%d')
            if datetime.now() - last_rain_date < timedelta(days=3):
                return True
    return False

def update_last_rain_date():
    with open(FILE_PATH, 'w') as file:
        json.dump({'last_rain_date': datetime.now().strftime('%Y-%m-%d')}, file)

def check_rain():
    weather = get_weather()
    if weather:
        if 'rain' in weather['weather'][0]['main'].lower():
            print("It has rained recently, no need to water the plants.")
            update_last_rain_date()
        else:
            if has_rained_recently():
                print("It hasn't rained for 3 days, but it rained recently.")
            else:
                print("It hasn't rained for 3 days! Remember to water your plants.")
    else:
        print("Unable to fetch weather data.")

if __name__ == '__main__':
    check_rain()
