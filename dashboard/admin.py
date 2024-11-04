from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(WeatherData)
admin.site.register(SolarGenerationData)
admin.site.register(PredictedSolarEnergy)
admin.site.register(PredictedPerformance)

