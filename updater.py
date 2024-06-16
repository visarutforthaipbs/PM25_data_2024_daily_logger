import requests
import json
from datetime import datetime

# API endpoint URL
url = "http://air4thai.com/forweb/getAQI_JSON.php"

# Perform a GET request to the API
response = requests.get(url)
response.raise_for_status()  # Raise an error if the request fails

# Parse the JSON data
data = response.json()

# Extract the list of stations
stations_data = data.get('stations', [])

# Prepare data to save
daily_data = []

for station in stations_data:
    station_id = station.get('stationID', 'N/A')
    station_name = station.get('nameTH', 'N/A')
    aqi_data = station.get('AQILast', {})
    pm25_value = aqi_data.get('PM25', {}).get('value', 'N/A')
    date = aqi_data.get('date', 'N/A')
    time = aqi_data.get('time', 'N/A')
    
    station_info = {
        "stationID": station_id,
        "nameTH": station_name,
        "date": date,
        "time": time,
        "pm25": pm25_value
    }
    daily_data.append(station_info)

# Get current date to create a new JSON file
current_date = datetime.now().strftime("%Y-%m-%d")

# Save data to a JSON file
with open(f'pm25_data_{current_date}.json', 'w', encoding='utf-8') as json_file:
    json.dump(daily_data, json_file, ensure_ascii=False, indent=4)

print(f"Data saved to pm25_data_{current_date}.json")
