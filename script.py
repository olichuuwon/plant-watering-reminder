"""
Api key have set a limit of 50 requests per day
Api key to be kept in a safe place (env/removed)

Use Task Scheduler
In the Actions pane, click Create Task.

General Tab:
Give your task a name (e.g., Run Python Script).
Choose Configure for: Windows 10.

Triggers Tab:
Click New and set Begin the task to At log on.

Actions Tab:
Click new and set Action to Start a program.
In the Program/script field, add the path to your python.exe.
In the Add arguments field, add the full path to your Python script.
"""

# Standard Library Imports
import os
import time
import socket
from datetime import datetime, timedelta
import ctypes

# Third-Party Library Imports
import requests
from dotenv import load_dotenv

load_dotenv()
STATION_ID = os.getenv("STATION_ID")
API_KEY = os.getenv("API_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")

NOW = datetime.now()
NOW_DATE = NOW.strftime("%Y-%m-%d")
ONE_DAY_AGO = NOW - timedelta(days=1)
ONE_DAY_AGO_DATE = ONE_DAY_AGO.strftime("%Y-%m-%d")
TWO_DAYS_AGO = NOW - timedelta(days=2)
TWO_DAYS_AGO_DATE = TWO_DAYS_AGO.strftime("%Y-%m-%d")
DATE = TWO_DAYS_AGO.strftime("%Y-%m-%d")


def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Plant Watering Reminder", 1)


def get_weather_openweathermap():
    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={LAT}&lon={LON}&date={DATE}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def get_weather_datagov(day):
    url = f"https://api-open.data.gov.sg/v2/real-time/api/rainfall?date={day}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        # print(f"Error: {response.status_code} - {response.text}")
        show_alert(f"Status code: {response.status_code}")
        return None


def rainfall_message(precipitation):
    if precipitation <= 5:
        message = """0 to 5 mm \n\nMinimal rainfall; likely need to water."""
    elif 5 < precipitation <= 10:
        message = """5 to 10 mm \n\nLight rain; check soil moisture. If dry, water your plants."""
    elif 10 < precipitation <= 20:
        message = """10 to 20 mm \n\nModerate rainfall; often sufficient moisture. Check the top inch of soil."""
    else:
        message = """More than 20 mm \n\nSignificant rainfall; usually no need to water unless the soil drains poorly."""
    return message


def is_connected():
    try:
        # Try to connect to a public DNS server
        socket.create_connection(("8.8.8.8", 53))  # Google Public DNS
        return True
    except OSError:
        return False


def wait_for_internet():
    while not is_connected():
        time.sleep(5)  # Wait for 5 seconds before checking again


def main_openweathermap():
    wait_for_internet()
    weather_json = get_weather_openweathermap()
    if weather_json is not None:
        total_precipitation = weather_json["precipitation"]["total"]
        show_alert(
            f"Total precipitation: {total_precipitation} mm\n\n{rainfall_message(total_precipitation)}"
        )


def main_datagov():
    wait_for_internet()
    total_percipitation = 0

    day_json = get_weather_datagov(NOW_DATE)
    data_list = day_json["data"]["readings"]  # type: ignore
    for item in data_list:
        # print(item)
        station_list = item["data"]
        for station in station_list:
            if station["stationId"] == STATION_ID:
                total_percipitation += station["value"]

    day_json = get_weather_datagov(ONE_DAY_AGO_DATE)
    data_list = day_json["data"]["readings"]  # type: ignore
    for item in data_list:
        # print(item)
        station_list = item["data"]
        for station in station_list:
            if station["stationId"] == STATION_ID:
                total_percipitation += station["value"] / 2

    day_json = get_weather_datagov(TWO_DAYS_AGO_DATE)
    data_list = day_json["data"]["readings"]  # type: ignore
    for item in data_list:
        # print(item)
        station_list = item["data"]
        for station in station_list:
            if station["stationId"] == STATION_ID:
                total_percipitation += station["value"] / 3

    show_alert(
        f"Total precipitation: {total_percipitation} mm\n\n{rainfall_message(total_percipitation)}"
    )


if __name__ == "__main__":
    main_datagov()
    # main_openweathermap()
