# Generated by Django 5.0.7 on 2024-09-30 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PredictedPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('predicted_energy', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SolarGenerationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('energy_generated', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('temperature', models.FloatField()),
                ('condition', models.CharField(max_length=100)),
                ('wind_speed', models.FloatField()),
                ('wind_direction', models.CharField(max_length=10)),
                ('pressure', models.FloatField()),
                ('precipitation', models.FloatField()),
                ('humidity', models.IntegerField()),
                ('cloud', models.IntegerField()),
                ('uv', models.FloatField()),
            ],
        ),
    ]