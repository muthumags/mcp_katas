# Air Quality MCP Server

This project is a **FastMCP server** that provides real-time air quality data for Indian cities using the **AQICN API**. It exposes multiple tools for your MCP clients:

- `get_air_quality(city)` → Current AQI, dominant pollutant, AQI category
- `get_pollutants(city)` → Pollutant breakdown (PM2.5, PM10, O₃, NO₂, CO, SO₂, etc.)
- `get_forecast(city)` → Short-term AQI forecast (daily min/avg/max)

---

## ⚡ Requirements

- Python 3.10+
- [uv](https://astral.sh/uv) package manager
- AQICN API token (sign up here: https://aqicn.org/data-platform/token/)

---

## 💾 Setup Instructions

### 1️⃣ Clone / Navigate to project folder
```bash

cd mcp_katas
add .env file and add AQICN_API_TOKEN along with the token 
uv sync
6️⃣ Run the MCP server

uv run main.py
Server will start and expose all tools for MCP clients.

or 
npx @modelcontextprotocol/inspector uv run main.py
MCP Inspector will start


🔧 Example MCP Tool Calls
Get current air quality
json
Copy code
{
  "tool": "get_air_quality",
  "input": { "city": "Chennai" }
}
Get pollutant details
json
Copy code
{
  "tool": "get_pollutants",
  "input": { "city": "Chennai" }
}
Get forecast
json
Copy code
{
  "tool": "get_forecast",
  "input": { "city": "Chennai" }
}
✅ Notes
Free AQICN tokens have request limits — consider caching results if needed.

Use .env and .gitignore to keep your token safe.

Forecast availability depends on city and AQICN coverage.

📚 References
AQICN API Documentation

FastMCP Documentation

uv Package Manager