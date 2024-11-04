


def calculate_solar_energy(system_size, avg_peak_sun_hours, cloud_cover):
    """
    Calculate solar energy production based on system size, peak sun hours, and cloud cover.
    The cloud cover impacts the total energy produced; higher cloud cover lowers the energy output.
    """
    # Assuming 100% cloud cover reduces energy output by 50%, adjust as needed.
    cloud_effect = 1 - (cloud_cover / 200)  # 50% reduction at full cloud cover (100%)
    cloud_effect = max(cloud_effect, 0.5)  # Ensure the energy doesn't drop below 50%
    
    # Calculate energy generation adjusted for cloud cover
    energy_production = system_size * avg_peak_sun_hours * cloud_effect
    return energy_production
