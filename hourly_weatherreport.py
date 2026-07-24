import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse



def generate_hourly_weather_report (lat,lon):
    

# Kolkata coordinates
# latitude = 22.5726
# longitude = 88.3639

# Last 30 days
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

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "humidity": data["hourly"]["relative_humidity_2m"],
        "rain": data["hourly"]["precipitation"]
    })

    df.to_csv("hourly_weather.csv", index=False)
    print("CSV saved successfully!")
    print(df.head())
    



def generate_all_hourly_weather_report (lat,lon):
    

# Kolkata coordinates
# latitude = 22.5726
# longitude = 88.3639

# Last 30 days
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

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame({
    "time": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "humidity": data["hourly"]["relative_humidity_2m"],
    "feels_like": data["hourly"]["apparent_temperature"],
    "wind_speed": data["hourly"]["wind_speed_10m"],
    "wind_direction": data["hourly"]["wind_direction_10m"],
    "wind_gusts": data["hourly"]["wind_gusts_10m"],
    "weather_code": data["hourly"]["weather_code"],
    "cloud_cover": data["hourly"]["cloud_cover"],
    "precipitation": data["hourly"]["precipitation"],
    "rain": data["hourly"]["rain"],
    "showers": data["hourly"]["showers"],
    "snowfall": data["hourly"]["snowfall"],
    "surface_pressure": data["hourly"]["surface_pressure"],
    "visibility": data["hourly"]["visibility"]
})

    df.to_csv("hourly_all_weather.csv", index=False)
    print("CSV saved successfully!")
    print(df.head())
    
    
    
if __name__=="__main__":
    
    # Kolkata coordinates
    latitude = 22.5726
    longitude = 88.3639
    
    generate_hourly_weather_report(latitude,longitude)
    generate_all_hourly_weather_report(latitude,longitude)
    