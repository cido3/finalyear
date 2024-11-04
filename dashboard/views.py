import json
from venv import logger
import requests
from random import uniform
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from dashboard.models import Notification, PredictedSolarEnergy, SolarGenerationData

API_KEY = 'e76e5d8617ae41e681093652242507'  # Replace with your actual WeatherAPI.com API key
BASE_URL = 'http://api.weatherapi.com/v1'

def fetch_forecast_data(location, days):
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={location}&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        for day in data['forecast']['forecastday']:
            # Average cloud cover over all hours
            cloud_cover_sum = sum([hour['cloud'] for hour in day['hour']])
            avg_cloud_cover = cloud_cover_sum / len(day['hour'])

            forecast_data.append({
                'date': day['date'],
                'max_temp': day['day']['maxtemp_c'],
                'cloud': avg_cloud_cover  # Now using average cloud cover from hourly data
            })
        return forecast_data
    else:
        raise Exception(f"Error fetching forecast data: {response.status_code}")


def calculate_solar_energy(cloud_cover):
    """
    Simplified logic: Less cloud cover means higher expected solar energy.
    Assume ideal solar generation without cloud cover is 25 kWh.
    """
    base_energy = 2.0
    cloud_effect = 1 - (cloud_cover / 100)  # Full cloud cover reduces energy to 0%
    predicted_energy = base_energy * max(cloud_effect, 0.5)  # Minimum 50% generation
    return predicted_energy

@login_required
def dashboard(request):
    today = timezone.now().date()

    # Fetch forecast for the next 6 days (including today)
    forecast_data = fetch_forecast_data('Lusaka', 3)  # Change to 6 days
    unread_notifications = Notification.objects.filter(is_read=False).order_by('-timestamp')
    weather_labels = []
    weather_temps = []
    weather_clouds = []
    actual_solar_energy = []
    expected_solar_energy = []

    # Variables to hold the predictions for today and tomorrow
    today_prediction = None
    tomorrow_prediction = None

    for forecast in forecast_data:
        weather_labels.append(forecast['date'])
        weather_temps.append(forecast['max_temp'])
        weather_clouds.append(forecast['cloud'])

        prediction_record, created = PredictedSolarEnergy.objects.get_or_create(
            date=forecast['date'],  # Directly using forecast['date']
            defaults={
                'system_size': 5.0,  # System size default, you can adjust it as needed
                'peak_sun_hours': 5,  # Just an example, adjust as needed
                'predicted_energy': 0.0,  # Initialize with 0, will be updated later
            }
        )

        # Only generate actual energy for the current day
        if forecast['date'] == str(today):
            actual_energy = uniform(1.0, 2.0)
            actual_solar_energy.append(actual_energy)

            # Save the actual generated energy into the model
            SolarGenerationData.objects.create(
                timestamp=timezone.now(),
                energy_generated=actual_energy
            )
            prediction_record.actual_energy = actual_energy
            prediction_record.save()

        # Calculate predicted energy based on cloud cover
        predicted_energy = calculate_solar_energy(forecast['cloud'])
        expected_solar_energy.append(predicted_energy)

        # Set today's prediction
        if forecast['date'] == str(today):
            today_prediction = predicted_energy
        # Set tomorrow's prediction
        elif forecast['date'] == str(today + timedelta(days=1)):
            tomorrow_prediction = predicted_energy

    current_weather = fetch_current_weather('Lusaka')

    context = {
        'current_weather': current_weather,
        'weather_labels': json.dumps(weather_labels),
        'weather_temps': json.dumps(weather_temps),
        'weather_clouds': json.dumps(weather_clouds),
        'actual_solar_energy': json.dumps(actual_solar_energy),
        'expected_solar_energy': json.dumps(expected_solar_energy),
        'unread_notifications': unread_notifications,
        'predicted_performance': {
            'today': today_prediction,
            'tomorrow': tomorrow_prediction,
        }
    }

    return render(request, 'dashboard/dashboard.html', context)

def fetch_current_weather(location):
    try:
        url = f"{BASE_URL}/current.json?key={API_KEY}&q={location}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        weather_data = {
            'temperature': data['current']['temp_c'],
            'condition': data['current']['condition']['text'],
            'cloud': data['current']['cloud'],
            'wind_speed': data['current']['wind_kph'],  # Added wind speed
            'humidity': data['current']['humidity'],    # Added humidity
            'uv': data['current']['uv'],                # Added UV index
        }
        return weather_data

    except requests.exceptions.HTTPError as http_err:
        # Log the error and response details
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
        return {
            'temperature': 'N/A',
            'condition': 'Service Unavailable',
            'cloud': 'N/A',
            'wind_speed': 'N/A',
            'humidity': 'N/A',
            'uv': 'N/A',
        }

    except Exception as err:
        # Handle any other exceptions (like network issues)
        print(f"Error fetching current weather: {err}")
        return {
            'temperature': 'N/A',
            'condition': 'Service Unavailable',
            'cloud': 'N/A',
            'wind_speed': 'N/A',
            'humidity': 'N/A',
            'uv': 'N/A',
        }


def analytics(request):
    predictions = PredictedSolarEnergy.objects.all()  # Retrieve all predictions
    threshold = 30  # e.g., 10% discrepancy threshold
    weather_labels = []
    actual_solar_energy = []
    expected_solar_energy = []
    prediction_accuracy = []
    unread_notifications = Notification.objects.filter(is_read=False).order_by('-timestamp')

    for prediction in predictions:
        weather_labels.append(str(prediction.date))
        
        # Replace None with 0 in actual energy
        actual_energy = prediction.actual_energy if prediction.actual_energy is not None else 0.0
        predicted_energy = prediction.predicted_energy if prediction.predicted_energy is not None else 0.0

        actual_solar_energy.append(actual_energy)
        expected_solar_energy.append(predicted_energy)

        # Calculate accuracy only if both actual and predicted energy are greater than 0
        if actual_energy > 0 and predicted_energy > 0:
            accuracy = (min(actual_energy, predicted_energy) / max(actual_energy, predicted_energy)) * 100
            prediction_accuracy.append(round(accuracy, 2))
        else:
            prediction_accuracy.append(0)  # Set to 0 if either value is missing or zero

    # Calculate discrepancies
    discrepancies = []
    for actual, predicted in zip(actual_solar_energy, expected_solar_energy):
        if actual is not None and predicted is not None:
            discrepancy = abs(actual - predicted) / predicted * 100  # Calculate percentage discrepancy
            discrepancies.append(discrepancy)

    # Calculate the average discrepancy
    average_discrepancy = sum(discrepancies) / len(discrepancies) if discrepancies else 0
    discrepancy_status = "Normal" if average_discrepancy < threshold else "High Discrepancy"

    if average_discrepancy >= threshold:
        Notification.objects.create(
            message=f"Discrepancy alert: Average discrepancy of {average_discrepancy:.2f}% exceeds the threshold.",
        )

    # Pass data to the context
    context = {
        'weather_labels': weather_labels,
        'actual_solar_energy': actual_solar_energy,
        'expected_solar_energy': expected_solar_energy,
        'prediction_accuracy': prediction_accuracy,
        'average_discrepancy': round(average_discrepancy, 2),
        'unread_notifications': unread_notifications,
        'discrepancy_status': discrepancy_status,
    }

    return render(request, 'dashboard/analytics.html', context)


def mark_notification_as_read(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.is_read = True
    notification.save()
    return redirect('analytics')  # Redirect back to the analytics page

def delete_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.delete()
    return redirect('analytics')  # Redirect back to the analytics page
