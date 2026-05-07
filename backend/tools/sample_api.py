import httpx
from  langchain_core.tools import tool

@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get the weather for a location given its coordinates.
    
    Args:
        latitude: The latitude of the location.(e.g 40.4 for princeton, NJ)
        longitude: The longitude of the location.(e.g -74.6 for princeton, NJ)
    
    Returns:
        Current temperature in Fahrenheit and weather code.
    """
    url = f"https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "temperature_unit": "fahrenheit"
    }
    response = httpx.get(url, params=params, timeout=10)
    response.raise_for_status()
    weather = response.json()["current_weather"]
    return f"The current temperature is {weather['temperature']} degrees in Fahrenheit, wind speed is {weather['windspeed']}km/h and the weather code is {weather['weathercode']}."


