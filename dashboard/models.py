from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=10)
    pressure = models.FloatField()
    precipitation = models.FloatField()
    humidity = models.IntegerField()
    cloud = models.IntegerField()
    uv = models.FloatField()

# ... other models ...

class SolarGenerationData(models.Model):
    timestamp = models.DateTimeField()
    energy_generated = models.FloatField()

class PredictedPerformance(models.Model):
    timestamp = models.DateTimeField()
    predicted_energy = models.FloatField()

class PredictedSolarEnergy(models.Model):
    date = models.DateField(unique=True)
    system_size = models.FloatField(default=5.0)  # in kW
    peak_sun_hours = models.FloatField(default=5.0)
    predicted_energy = models.FloatField()
    actual_energy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Prediction for {self.date}: {self.predicted_energy:.2f} kWh"
    

class Notification(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification at {self.timestamp}: {self.message}"
