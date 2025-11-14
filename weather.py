# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')


from typing import Any
import httpx
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """Get complete weather information for a location (US only).

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    Exemple:
        weather_report = await get_weather(40.7128, -74.0060)
    """
    # Step 1: Get location info and URLs
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return f"❌ Unable to fetch weather data for location ({latitude}, {longitude}). Location may not be in the US."
    
    # Extract location information
    properties = points_data["properties"]
    city = properties.get("relativeLocation", {}).get("properties", {}).get("city", "Unknown")
    state = properties.get("relativeLocation", {}).get("properties", {}).get("state", "Unknown")
    
    # Get all weather data URLs
    forecast_url = properties.get("forecast")
    stations_url = properties.get("observationStations")
    
    report = f"""
🌦️ WEATHER REPORT FOR {city.upper()}, {state}
📍 Coordinates: {latitude}, {longitude}
⏰ Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
    
    # Step 2: Get current conditions
    if stations_url:
        stations_data = await make_nws_request(stations_url)
        if stations_data and stations_data.get("features"):
            station_id = stations_data["features"][0]["properties"]["stationIdentifier"]
            observations_url = f"{NWS_API_BASE}/stations/{station_id}/observations/latest"
            obs_data = await make_nws_request(observations_url)
            
            if obs_data:
                props = obs_data["properties"]
                temp_c = props.get("temperature", {}).get("value")
                temp_f = (temp_c * 9/5) + 32 if temp_c is not None else None
                humidity = props.get("relativeHumidity", {}).get("value")
                wind_speed = props.get("windSpeed", {}).get("value")
                wind_dir = props.get("windDirection", {}).get("value")
                description = props.get("textDescription", "N/A")
                
                report += "🌡️ CURRENT CONDITIONS:\n"
                if temp_f and temp_c:
                    report += f"   Temperature: {temp_f:.1f}°F ({temp_c:.1f}°C)\n"
                if humidity:
                    report += f"   Humidity: {humidity:.0f}%\n"
                if wind_speed:
                    wind_dir_text = f" from {wind_dir:.0f}°" if wind_dir else ""
                    report += f"   Wind: {wind_speed:.1f} m/s{wind_dir_text}\n"
                report += f"   Conditions: {description}\n"
                report += f"   Station: {station_id}\n\n"
    
    # Step 3: Get forecast
    if forecast_url:
        forecast_data = await make_nws_request(forecast_url)
        if forecast_data:
            periods = forecast_data["properties"].get("periods", [])
            
            report += "� 7-DAY FORECAST:\n"
            for period in periods[:7]:
                is_day = period.get('isDaytime', True)
                icon = "☀️" if is_day else "🌙"
                temp = period.get('temperature', 'N/A')
                temp_unit = period.get('temperatureUnit', '')
                short_forecast = period.get('shortForecast', 'N/A')
                
                report += f"   {icon} {period['name']}: {temp}°{temp_unit} - {short_forecast}\n"
            report += "\n"
    
    # Step 4: Get alerts for the state
    if state and state != "Unknown":
        alerts_url = f"{NWS_API_BASE}/alerts/active/area/{state}"
        alerts_data = await make_nws_request(alerts_url)
        
        if alerts_data and alerts_data.get("features"):
            alert_count = len(alerts_data["features"])
            report += f"🚨 ACTIVE ALERTS ({alert_count}):\n"
            
            for feature in alerts_data["features"][:5]:  # Show first 5 alerts
                props = feature["properties"]
                event = props.get('event', 'Unknown')
                severity = props.get('severity', 'Unknown')
                area = props.get('areaDesc', 'Unknown')
                
                report += f"   ⚠️ {event} ({severity})\n"
                report += f"      Area: {area}\n"
        else:
            report += "✅ No active alerts\n"
    
    report += f"\n{'='*60}\nData source: National Weather Service (weather.gov)"
    
    return report


if __name__ == "__main__":
    print("🌦️ Weather MCP Server starting...")
    print("� Available tool: get_weather")
    print("🇺🇸 Note: Works only for US locations")
    #
    try:
        mcp.run(transport='stdio')
        #Affichage dans le terminal les infos du weather
        print("🌦️ Weather MCP Server running...")
        
    except KeyboardInterrupt:
        print("\n👋 Weather MCP Server stopped")
    except Exception as e:
        print(f"❌ Server error: {str(e)}")

