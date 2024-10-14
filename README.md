# Plant Watering Reminder

This project is a Python script that provides plant watering reminders based on recent rainfall data from public APIs, primarily using Data.gov.sg. The script calculates total precipitation over the past few days and sends notifications via a system alert box to help determine whether your plants need watering.

## Features
- Retrieves real-time and past rainfall data from the **Data.gov.sg** API using station-specific rainfall measurements.
- Supports OpenWeatherMap API (though less accurate due to patchy weather conditions in some areas).
- Uses Windows Task Scheduler to automate script execution at system logon.
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

### API Key and Station ID Setup
1. Obtain a **Station ID** from [Data.gov.sg](https://data.gov.sg) for your nearest weather station.
2. Optionally, obtain an API key from [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) if you want to use it as a fallback.
3. Set the following environment variables in a `.env` file or directly in your system:
   - `STATION_ID` (Required for Data.gov.sg)
   - `API_KEY` (Optional for OpenWeatherMap)
   - `LAT` (Latitude, required for OpenWeatherMap)
   - `LON` (Longitude, required for OpenWeatherMap)

#### Example `.env` File:
```
STATION_ID=your_station_id
API_KEY=your_openweather_api_key   # Optional
LAT=your_latitude   # Required if using OpenWeatherMap
LON=your_longitude  # Required if using OpenWeatherMap
```

### Important Note on OpenWeatherMap:
- OpenWeatherMap data might be less reliable in regions with patchy or localized weather conditions. It's recommended to use **Data.gov.sg** for more precise rainfall data where available.
- A **hard cap** has been placed on the OpenWeatherMap website itself to prevent exceeding the free tier limit of 50 requests per day, avoiding potential charges.

## Usage

### Running the Script
To manually run the script, execute:
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
- `get_weather_datagov(day)`: Retrieves rainfall data from Data.gov.sg for a specific date using the provided `STATION_ID`.
- `get_weather_openweathermap()`: (Optional) Fetches weather data from OpenWeatherMap.
- `rainfall_message(precipitation)`: Provides watering instructions based on total precipitation.
- `is_connected()`: Checks for an internet connection.
- `wait_for_internet()`: Pauses execution until an internet connection is available.
- `show_alert(message)`: Displays a system message box to alert the user.

### Example Alert:
- For rainfall between 0 and 5 mm:  
  *"Minimal rainfall; likely need to water."*
  
- For rainfall over 20 mm:  
  *"Significant rainfall; usually no need to water unless the soil drains poorly."*

## Notes
- **OpenWeatherMap API Usage**: The script will not exceed the free tier limit of 50 requests/day due to a hard cap set on the OpenWeatherMap account, ensuring you don't get charged for additional requests.
- The script defaults to Data.gov.sg for better precision using the station-specific rainfall measurements.

## License
This project is open-source and available under the [MIT License](LICENSE).
