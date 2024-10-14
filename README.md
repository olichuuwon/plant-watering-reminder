# Plant Watering Reminder

This project is a Python script that provides plant watering reminders based on recent rainfall data from public APIs (Data.gov.sg or OpenWeatherMap). The script calculates total precipitation over the past few days and sends notifications via a system alert box.

## Features
- Retrieves real-time and past rainfall data from the Data.gov.sg or OpenWeatherMap API.
- Uses the Task Scheduler in Windows to automate script execution at system logon.
- Alerts users with a pop-up message containing watering advice based on total precipitation.

## Setup

### Prerequisites
- Python 3.x
- Required libraries:
  - `requests`
  - `python-dotenv`
  
Install the dependencies with:
```bash
pip install requests python-dotenv
```

### API Key Setup
1. Obtain an API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) and set the necessary environmental variables for:
   - `STATION_ID`
   - `API_KEY`
   - `LAT` (Latitude)
   - `LON` (Longitude)

2. Store these keys safely, either in a `.env` file or set them as environment variables.

#### `.env` Example:
```
STATION_ID=your_station_id
API_KEY=your_openweather_api_key
LAT=your_latitude
LON=your_longitude
```

## Usage

### Running the Script
To manually run the script, simply execute:
```bash
python your_script.py
```

### Scheduling the Script to Run Automatically (Windows)
1. Open **Task Scheduler**.
2. In the **Actions** pane, click **Create Task**.
3. **General Tab**: Give your task a name (e.g., "Plant Watering Reminder").
4. **Triggers Tab**: Click **New** and set **Begin the task** to **At log on**.
5. **Actions Tab**:
   - Set **Action** to **Start a program**.
   - In the **Program/script** field, add the path to `python.exe`.
   - In the **Add arguments** field, add the full path to your Python script.
6. Save the task.

## Functionality

### Key Functions:
- `get_weather_openweathermap()`: Fetches weather data from OpenWeatherMap.
- `get_weather_datagov(day)`: Retrieves rainfall data from Data.gov.sg for a specific date.
- `rainfall_message(precipitation)`: Determines watering instructions based on precipitation.
- `is_connected()`: Checks for an internet connection.
- `wait_for_internet()`: Pauses execution until an internet connection is available.
- `show_alert(message)`: Displays a system message box to alert the user.

### Example Output:
- If rainfall is 0 to 5 mm:  
  *"Minimal rainfall; likely need to water."*
  
- If rainfall is 10 to 20 mm:  
  *"Moderate rainfall; often sufficient moisture. Check the top inch of soil."*

## Notes
- The OpenWeatherMap API has a limit of 50 requests per day, so use it judiciously.
- The script can handle different APIs by toggling between `main_openweathermap()` and `main_datagov()`.

## License
This project is open-source and available under the [MIT License](LICENSE).
