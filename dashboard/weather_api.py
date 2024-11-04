import requests
from datetime import datetime, timedelta
from django.utils import timezone

API_KEY = 'e76e5d8617ae41e681093652242507'  # Replace with your actual WeatherAPI.com API key
BASE_URL = 'http://api.weatherapi.com/v1'

def fetch_historical_weather_data(location, start_date, end_date):
    historical_data = []
    current_date = start_date

    while current_date <= end_date:
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={current_date.strftime('%Y-%m-%d')}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            #print(data)  # Debugging line to check the structure of the response
            day_data = {
                'date': current_date.strftime('%Y-%m-%d'),
                'max_temp': data['forecast']['forecastday'][0]['day']['maxtemp_c'],
                'cloud': data['forecast']['forecastday'][0]['day'].get('cloud', 0),  # Use .get() to avoid KeyError
            }
            historical_data.append(day_data)
        else:
            raise Exception(f"Error fetching historical weather data: {response.status_code}")
        
        current_date += timedelta(days=1)

    return historical_data

def fetch_current_weather(location):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'wind_speed': data['current']['wind_kph'],
            'wind_direction': data['current']['wind_dir'],
            'pressure': data['current']['pressure_mb'],
            'precipitation': data['current']['precip_mm'],
            'humidity': data['current']['humidity'],
            'cloud': data['current']['cloud'],
            'uv': data['current']['uv']
        }
        return weather_data
    else:
        raise Exception(f"Error fetching current weather data: {response.status_code}")



def fetch_forecast_data(location, days=3):
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        for day in data['forecast']['forecastday']:
            # Instead of averaging, let's grab the cloud cover for midday (e.g., 12 PM) as a simple solution
            midday_data = next((hour for hour in day['hour'] if hour['time'].endswith('12:00')), None)
            cloud_cover = midday_data['cloud'] if midday_data else 0  # Default to 0 if no midday data

            forecast_data.append({
                'date': day['date'],
                'max_temp': day['day']['maxtemp_c'],
                'min_temp': day['day']['mintemp_c'],
                'avg_humidity': day['day']['avghumidity'],
                'condition': day['day']['condition']['text'],
                'cloud': cloud_cover,  # Grab the cloud cover at 12 PM
                'precipitation': day['day']['totalprecip_mm'],
            })
        return forecast_data
    else:
        raise Exception(f"Error fetching forecast data: {response.status_code}")
