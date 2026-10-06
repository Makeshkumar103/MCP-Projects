import os
import httpx
from typing import Any
from mcp.server.mcpserver import MCPServer
from mcp.types import TextContent


server = MCPServer("weather-mcp-server")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"


async def get_weather_data(endpoint: str, params: dict) -> dict:
    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")

    params["appid"] = OPENWEATHER_API_KEY
    params["units"] = "metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()


def build_location_params(city: str = "", country_code: str = "", lat: float = None, lon: float = None) -> dict:
    params = {}
    if lat is not None and lon is not None:
        params["lat"] = lat
        params["lon"] = lon
    elif city:
        q = city
        if country_code:
            q += f",{country_code}"
        params["q"] = q
    return params


def format_current_weather(data: dict) -> str:
    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind = data.get("wind", {})
    sys = data.get("sys", {})

    return f"""Current Weather for {data.get('name', 'Unknown')}, {sys.get('country', 'Unknown')}:
Temperature: {main.get('temp', 'N/A')}°C (Feels like: {main.get('feels_like', 'N/A')}°C)
Min/Max: {main.get('temp_min', 'N/A')}°C / {main.get('temp_max', 'N/A')}°C
Humidity: {main.get('humidity', 'N/A')}%
Pressure: {main.get('pressure', 'N/A')} hPa
Condition: {weather.get('description', 'N/A').capitalize()}
Wind: {wind.get('speed', 'N/A')} m/s at {wind.get('deg', 'N/A')}°
Visibility: {data.get('visibility', 'N/A')} meters"""


def format_forecast(data: dict) -> str:
    city = data.get("city", {})
    forecasts = data.get("list", [])

    result = f"5-Day Forecast for {city.get('name', 'Unknown')}, {city.get('country', 'Unknown')}:\n\n"

    daily = {}
    for item in forecasts:
        date = item["dt_txt"].split(" ")[0]
        if date not in daily:
            daily[date] = []
        daily[date].append(item)

    for date, items in list(daily.items())[:5]:
        temps = [i["main"]["temp"] for i in items]
        conditions = [i["weather"][0]["description"] for i in items]
        result += f"{date}:\n"
        result += f"  Temp: {min(temps):.1f}°C - {max(temps):.1f}°C\n"
        result += f"  Conditions: {', '.join(set(conditions))}\n\n"

    return result


@server.tool()
async def get_current_weather(city: str = "", country_code: str = "", lat: float = None, lon: float = None) -> str:
    """Get current weather for a location."""
    params = build_location_params(city=city, country_code=country_code, lat=lat, lon=lon)
    if not params:
        return "Error: Provide either city or lat/lon"
    data = await get_weather_data("weather", params)
    return format_current_weather(data)


@server.tool()
async def get_weather_forecast(city: str = "", country_code: str = "", lat: float = None, lon: float = None) -> str:
    """Get 5-day weather forecast for a location."""
    params = build_location_params(city=city, country_code=country_code, lat=lat, lon=lon)
    if not params:
        return "Error: Provide either city or lat/lon"
    data = await get_weather_data("forecast", params)
    return format_forecast(data)


@server.tool()
async def get_weather_by_zip(zip_code: str, country_code: str = "US") -> str:
    """Get current weather by ZIP/postal code."""
    params = {"zip": f"{zip_code},{country_code}"}
    data = await get_weather_data("weather", params)
    return format_current_weather(data)


if __name__ == "__main__":
    server.run()