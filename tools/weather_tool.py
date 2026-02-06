import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from tools.base_tool import BaseTool

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
        Fetch current weather for a specific city.
        
        Args:
            city (str): The name of the city.
            
        Returns:
            Dict: Weather data or error message.
        """
        if not self.api_key:
            return {"error": "Missing OPENWEATHER_API_KEY in environment variables."}

        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            response = requests.get(self.base_url, params=params)
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
            
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "details": response.text}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

if __name__ == "__main__":
    # Test the tool locally
    tool = WeatherTool()
    print(tool.execute(city="London"))
