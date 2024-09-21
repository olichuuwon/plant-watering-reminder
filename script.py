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

API_KEY = os.getenv("API_KEY")
LAT = 1.3667
LON = 103.8
NOW = datetime.now()
TWO_DAYS_AGO = NOW - timedelta(days=2)
DATE = TWO_DAYS_AGO.strftime("%Y-%m-%d")


def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Plant Watering Reminder", 1)


def get_weather():
    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={LAT}&lon={LON}&date={DATE}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def rainfall_message(precipitation):
    if precipitation <= 10:
        message = """0 to 10 mm (0 to 0.4 inches) \n\nMinimal rainfall; likely need to water."""
    elif 10 < precipitation <= 20:
        message = """10 to 20 mm (0.4 to 0.8 inches) \n\nLight rain; check soil moisture. If dry, water your plants."""
    elif 20 < precipitation <= 40:
        message = """20 to 40 mm (0.8 to 1.6 inches) \n\nModerate rainfall; often sufficient moisture. Check the top inch of soil."""
    else:
        message = """More than 40 mm (1.6 inches) \n\nSignificant rainfall; usually no need to water unless the soil drains poorly."""
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


def main():
    wait_for_internet()
    weather_json = get_weather()
    if weather_json is not None:
        total_precipitation = weather_json["precipitation"]["total"]
        show_alert(
            f"Total precipitation: {total_precipitation} mm\n\n{rainfall_message(total_precipitation)}"
        )


def see_json():
    print(get_weather())


if __name__ == "__main__":
    # see_json()
    main()
