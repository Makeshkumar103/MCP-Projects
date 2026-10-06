# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the OpenWeatherMap API.

## Features

- Get current weather by city name or coordinates
- Get 5-day weather forecast
- Get weather by ZIP/postal code

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)

3. Set the environment variable:
```bash
export OPENWEATHER_API_KEY="your-api-key-here"
```

## Usage

Run the server:
```bash
weather-mcp-server
```

Or with Python directly:
```bash
python -m weather_mcp_server
```

## Available Tools

- `get_current_weather` - Current weather for a location (city or lat/lon)
- `get_weather_forecast` - 5-day forecast for a location
- `get_weather_by_zip` - Current weather by ZIP code

## Example Queries

- "What's the weather in London, UK?"
- "Get the forecast for New York"
- "Weather for ZIP code 90210"