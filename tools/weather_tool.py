import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from tools.base_tool import BaseTool
from tools.retry_utils import api_retry

load_dotenv()

class WeatherTool(BaseTool):
    """
    Tool to fetch weather data from OpenWeatherMap.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def execute(self, city: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch current weather for a specific city with retry logic.
        
        Args:
            city (str): The name of the city.
            
        Returns:
            Dict: Weather data or error message.
        """
        if not self.api_key:
            return {"error": "Missing OPENWEATHER_API_KEY in environment variables."}

        try:
            return self._fetch_weather_with_retry(city)
        except Exception as err:
            print(f"[WeatherTool] All retry attempts failed: {err}")
            return {"error": f"Weather API failed after retries: {err}"}

    @api_retry
    def _fetch_weather_with_retry(self, city: str) -> Dict[str, Any]:
        """Internal method with retry decorator for API calls."""
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Celsius
        }
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Simplified output for the agent
        return {
            "status": "success",
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

if __name__ == "__main__":
    # Test the tool locally
    tool = WeatherTool()
    print(tool.execute(city="London"))
