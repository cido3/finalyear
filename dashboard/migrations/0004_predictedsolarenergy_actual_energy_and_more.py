# Generated by Django 5.0.7 on 2024-10-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_predictedsolarenergy'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictedsolarenergy',
            name='actual_energy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='predictedsolarenergy',
            name='peak_sun_hours',
            field=models.FloatField(default=5.0),
        ),
        migrations.AddField(
            model_name='predictedsolarenergy',
            name='system_size',
            field=models.FloatField(default=5.0),
        ),
    ]