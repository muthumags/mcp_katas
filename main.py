#!/usr/bin/env python3
import os
import requests
from mcp.server.fastmcp import FastMCP

import os
from dotenv import load_dotenv

# Load values from .env into system environment
load_dotenv()

AQICN_API_TOKEN = os.getenv("AQICN_API_TOKEN")
mcp = FastMCP("air-quality-server")


@mcp.tool()
def get_air_quality(city: str):
    """Get current AQI + dominant pollutant + AQI category."""
    data = fetch_data(city)
    if "error" in data:
        return data

    d = data["data"]
    return {
        "city": d["city"]["name"],
        "aqi": d["aqi"],
        "dominant_pollutant": d.get("dominentpol", "unknown"),
        "category": aqi_category(d["aqi"])
    }


@mcp.tool()
def get_pollutants(city: str):
    """Get current pollutant readings: PM2.5, PM10, O3, NO2, CO, SO2, etc."""
    data = fetch_data(city)
    if "error" in data:
        return data

    iaqi = data["data"].get("iaqi", {})
    pollutants = {
        key: val.get("v")
        for key, val in iaqi.items()
    }

    return {
        "city": data["data"]["city"]["name"],
        "pollutants": pollutants
    }


@mcp.tool()
def get_forecast(city: str):
    """Get next 3-5 days air quality forecast where available."""
    data = fetch_data(city)
    if "error" in data:
        return data

    forecast_data = data["data"].get("forecast", {}).get("daily", {})
    forecast_response = {}

    # Include pollutants if forecast data exists
    for pollutant, readings in forecast_data.items():
        forecast_response[pollutant] = [
            {
                "day": r.get("day"),
                "min": r.get("min"),
                "max": r.get("max"),
                "avg": r.get("avg")
            }
            for r in readings
        ]

    if not forecast_response:
        return {"error": "Forecast unavailable for this location"}

    return {
        "city": data["data"]["city"]["name"],
        "forecast": forecast_response
    }


def fetch_data(city: str):
    """Internal helper for API calls"""
    if not AQICN_API_TOKEN:
        return {"error": "Missing AQICN_API_TOKEN environment variable"}
    print(AQICN_API_TOKEN)
    url = f"https://api.waqi.info/feed/{city}/?token={AQICN_API_TOKEN}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"HTTP {response.status_code}"}

    data = response.json()
    if data.get("status") != "ok":
        return {"error": "City not found or invalid token", "details": data}

    return data


def aqi_category(aqi: int) -> str:
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Unhealthy for Sensitive Groups"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very Unhealthy"
    return "Hazardous"


if __name__ == "__main__":
    mcp.run()
