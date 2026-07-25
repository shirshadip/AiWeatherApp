import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse


def generate_30_day_report(lat,long):
    """Download last 30 days of daily weather for given coords and save CSV."""

    # Last 30 days
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={long}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,"
        f"precipitation_sum"
        f"&timezone=auto"
    )

    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)
        return
    data = response.json()
    if "daily" not in data:
        print("Unexpected API response: 'daily' key missing")
        return
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max": data["daily"]["temperature_2m_max"],
        "temp_min": data["daily"]["temperature_2m_min"],
        "rain_mm": data["daily"]["precipitation_sum"]
    })

    df.to_csv("weather_last_30_days.csv", index=False)

    print("CSV saved successfully!")
    print(df.head())
    
def generate_30_day_hum_wind_report(lat,long):
    """Download last 30 days of daily weather for given coords and save CSV."""

    # Last 30 days
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={long}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"wind_speed_10m_max"
        f"sunshine_duration"
        f"daylight_duration"
        f"&timezone=auto"
    )

    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print("Status Code:", response.status_code)
        print("Response:")
        print(response.text)
        return
    data = response.json()
    if "daily" not in data:
        print("Unexpected API response: 'daily' key missing")
        return
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max": data["daily"]["temperature_2m_max"],
        "temp_min": data["daily"]["temperature_2m_min"],
        "rain_mm": data["daily"]["precipitation_sum"]
    })

    df.to_csv("weather_last_30_days_hum_wind.csv", index=False)

    print("CSV saved successfully!")
    print(df.head())
    


def generate_30_day_daily_all_report(lat, long):
    """Download last 30 days of complete daily weather report."""

    from datetime import datetime, timedelta
    import requests
    import pandas as pd

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={long}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        f"&daily="
        f"temperature_2m_max,"
        f"temperature_2m_min,"
        f"apparent_temperature_max,"
        f"apparent_temperature_min,"
        f"precipitation_sum,"
        f"rain_sum,"
        f"showers_sum,"
        f"snowfall_sum,"
        f"precipitation_hours,"
        f"wind_speed_10m_max,"
        f"wind_gusts_10m_max,"
        f"wind_direction_10m_dominant,"
        f"sunrise,"
        f"sunset,"
        f"daylight_duration,"
        f"sunshine_duration,"
        f"weather_code"
        f"&timezone=auto"
    )

    response = requests.get(url)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        print("Status Code:", response.status_code)
        print(response.text)
        return

    data = response.json()

    if "daily" not in data:
        print("Unexpected API response.")
        return

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max": data["daily"]["temperature_2m_max"],
        "temp_min": data["daily"]["temperature_2m_min"],
        "feels_like_max": data["daily"]["apparent_temperature_max"],
        "feels_like_min": data["daily"]["apparent_temperature_min"],
        "precipitation_mm": data["daily"]["precipitation_sum"],
        "rain_mm": data["daily"]["rain_sum"],
        "showers_mm": data["daily"]["showers_sum"],
        "snowfall_cm": data["daily"]["snowfall_sum"],
        "precipitation_hours": data["daily"]["precipitation_hours"],
        "wind_speed_max": data["daily"]["wind_speed_10m_max"],
        "wind_gusts_max": data["daily"]["wind_gusts_10m_max"],
        "wind_direction": data["daily"]["wind_direction_10m_dominant"],
        "sunrise": data["daily"]["sunrise"],
        "sunset": data["daily"]["sunset"],
        "daylight_duration_sec": data["daily"]["daylight_duration"],
        "sunshine_duration_sec": data["daily"]["sunshine_duration"],
        "weather_code": data["daily"]["weather_code"]
    })

    # Thunderstorm column
    df["thunderstorm"] = df["weather_code"].isin([95, 96, 99]).map({
        True: "Yes",
        False: "No"
    })

    df.to_csv("weather_daily_all_report.csv", index=False)

    print("Daily weather report saved successfully!")
    print(df.head())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 30-day weather report CSV for coords")
    parser.add_argument("--lat", type=float, default=22.5726, help="Latitude (default: Kolkata)")
    parser.add_argument("--lon", type=float, default=88.3639, help="Longitude (default: Kolkata)")
    args = parser.parse_args()
    generate_30_day_report(args.lat, args.lon)
    generate_30_day_daily_all_report(args.lat, args.lon)
    generate_30_day_hum_wind_report(args.lat, args.lon)
    
    