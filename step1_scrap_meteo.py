import requests
import json
from datetime import datetime

def geocode_city(city: str, count: int = 1, language: str = "en") -> dict:
    """
    Fetch latitude and longitude for a given city using Open-Meteo Geocoding API.
    Returns location info (first result found).
    """
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city}&count={count}&language={language}&format=json"
    )
    print(f"[GEOCODING] Fetching coords for: {city}")
    print(f"[GEOCODING] URL: {url}")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to geocode city. Status code: {response.status_code}")
    results = response.json().get("results")
    if not results:
        raise Exception("No geocoding results found.")
    # Take the first result
    location = results[0]
    print(f"[GEOCODING] Success! Found: {location['name']} ({location['latitude']}, {location['longitude']})")
    return {
        "name": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }

def fetch_air_quality(lat: float, lon: float, forecast_days: int = 5) -> dict:
    """
    Fetch air quality forecast for given coordinates.
    Returns parsed air quality data.
    """
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=pm10,pm2_5,carbon_monoxide,carbon_dioxide,ozone"
        f"&past_days=0&forecast_days={forecast_days}"
    )
    print(f"[AIR QUALITY] Fetching AQ for lat={lat}, lon={lon}")
    print(f"[AIR QUALITY] URL: {url}")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch air quality. Status code: {response.status_code}")
    data = response.json()
    print("[AIR QUALITY] Success! Data keys:", list(data.keys()))
    # Only show first 3 hourly values for brevity
    hourly = data.get("hourly", {})
    hours = hourly.get("time", [])[:1]
    aq_summary = {
        "hourly_time": hours,
        "pm10": hourly.get("pm10", [])[:1],
        "pm2_5": hourly.get("pm2_5", [])[:1],
        "carbon_monoxide": hourly.get("carbon_monoxide", [])[:1],
        "carbon_dioxide": hourly.get("carbon_dioxide", [])[:1],
        "ozone": hourly.get("ozone", [])[:1],
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return aq_summary

def fetch_geocode_and_air_quality(city: str):
    """Orchestrates the geocoding and air quality fetching."""
    location = geocode_city(city)
    air_quality = fetch_air_quality(location["latitude"], location["longitude"])
    result = {
        "city": location["name"],
        "country": location["country"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "air_quality": air_quality,
    }
    return result

# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    city = "Kuala Lumpur"
    data = fetch_geocode_and_air_quality(city)
    print("\n── Air Quality Data ──")
    print(json.dumps(data, indent=2))

"""
def print_dict_types(d, prefix=""):
    for key, value in d.items():
        key_path = f"{prefix}.{key}" if prefix else key
        print(f"{key_path}: {type(value)}")
        if isinstance(value, dict):
            print_dict_types(value, key_path)

print_dict_types(data)"""