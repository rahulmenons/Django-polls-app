import csv
import os
import requests
from django.conf import settings
from datetime import datetime

def fetch_and_save_weather():
    """Fetch weather data from OpenWeather and save to CSV."""
    api_key = settings.OPENWEATHER_API_KEY
    city = settings.CITY

    if not api_key:
        raise ValueError("No API key found in environment variables")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    record = {
        'datetime': datetime.utcfromtimestamp(data['dt']).isoformat(),
        'temperature': data['main']['temp'],
        'condition': data['weather'][0]['main']
    }

    csv_file = os.path.join(os.path.dirname(__file__), 'weather_data.csv')
    header = ['datetime', 'temperature', 'condition']

    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    return record
