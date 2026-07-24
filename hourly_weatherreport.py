import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse



def generate_hourly_weather_report(lat, lon):
    """Download hourly weather data for the last 30 days and save it to CSV."""

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&hourly=temperature_2m,relative_humidity_2m,"
        f"precipitation"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Hourly weather request failed: {exc}")
        return False

    try:
        data = response.json()
        hourly_data = data["hourly"]
    except (ValueError, KeyError, TypeError) as exc:
        print(f"Unexpected hourly API response: {exc}")
        return False

    required_columns = {
        "time": "time",
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "precipitation": "rain",
    }

    missing_columns = [key for key in required_columns if key not in hourly_data]
    if missing_columns:
        print(f"Unexpected hourly API response: missing keys {missing_columns}")
        return False

    df = pd.DataFrame({
        "time": hourly_data["time"],
        "temperature": hourly_data["temperature_2m"],
        "humidity": hourly_data["relative_humidity_2m"],
        "rain": hourly_data["precipitation"],
    })

    df.to_csv("hourly_weather.csv", index=False)
    print("CSV saved successfully!")
    print(df.head())
    return True


def generate_all_hourly_weather_report(lat, lon):
    """Download a richer hourly weather dataset and save it to CSV."""

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&hourly="
        f"temperature_2m,"
        f"relative_humidity_2m,"
        f"apparent_temperature,"
        f"wind_speed_10m,"
        f"wind_direction_10m,"
        f"wind_gusts_10m,"
        f"weather_code,"
        f"cloud_cover,"
        f"precipitation,"
        f"rain,"
        f"showers,"
        f"snowfall,"
        f"surface_pressure,"
        f"visibility"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Hourly weather request failed: {exc}")
        return False

    try:
        data = response.json()
        hourly_data = data["hourly"]
    except (ValueError, KeyError, TypeError) as exc:
        print(f"Unexpected hourly API response: {exc}")
        return False

    required_columns = {
        "time": "time",
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "apparent_temperature": "feels_like",
        "wind_speed_10m": "wind_speed",
        "wind_direction_10m": "wind_direction",
        "wind_gusts_10m": "wind_gusts",
        "weather_code": "weather_code",
        "cloud_cover": "cloud_cover",
        "precipitation": "precipitation",
        "rain": "rain",
        "showers": "showers",
        "snowfall": "snowfall",
        "surface_pressure": "surface_pressure",
        "visibility": "visibility",
    }

    missing_columns = [key for key in required_columns if key not in hourly_data]
    if missing_columns:
        print(f"Unexpected hourly API response: missing keys {missing_columns}")
        return False

    df = pd.DataFrame({
        "time": hourly_data["time"],
        "temperature": hourly_data["temperature_2m"],
        "humidity": hourly_data["relative_humidity_2m"],
        "feels_like": hourly_data["apparent_temperature"],
        "wind_speed": hourly_data["wind_speed_10m"],
        "wind_direction": hourly_data["wind_direction_10m"],
        "wind_gusts": hourly_data["wind_gusts_10m"],
        "weather_code": hourly_data["weather_code"],
        "cloud_cover": hourly_data["cloud_cover"],
        "precipitation": hourly_data["precipitation"],
        "rain": hourly_data["rain"],
        "showers": hourly_data["showers"],
        "snowfall": hourly_data["snowfall"],
        "surface_pressure": hourly_data["surface_pressure"],
        "visibility": hourly_data["visibility"],
    })

    df.to_csv("hourly_all_weather.csv", index=False)
    print("CSV saved successfully!")
    print(df.head())
    return True
    
    
    
if __name__=="__main__":
    
    # Kolkata coordinates
    latitude = 22.5726
    longitude = 88.3639
    
    generate_hourly_weather_report(latitude,longitude)
    generate_all_hourly_weather_report(latitude,longitude)
    