import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from tools.base_tool import BaseTool

load_dotenv()

class NewsTool(BaseTool):
    """
    Tool to fetch news related to travel safety/disruptions from NewsData.io.
    """
    def __init__(self):
        self.api_key = os.getenv("NEWSDATA_API_KEY")
        self.base_url = "https://newsdata.io/api/1/news"

    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch news articles based on a query.
        
        Args:
            query (str): Search query (e.g., "Delhi travel safety strike").
            
        Returns:
            Dict: List of news articles or error message.
        """
        if not self.api_key:
            return {"error": "Missing NEWSDATA_API_KEY in environment variables."}

        try:
            params = {
                "apikey": self.api_key,
                "q": query,
                "language": "en"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "success":
                return {"error": f"API returned error: {data.get('results')}"}
                
            results = data.get("results", [])
            simplified_results = []
            
            for article in results[:5]: # Top 5 articles
                simplified_results.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "link": article.get("link"),
                    "pubDate": article.get("pubDate")
                })
                
            return {
                "status": "success",
                "totalResults": data.get("totalResults"),
                "articles": simplified_results
            }
            
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "details": response.text}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

if __name__ == "__main__":
    tool = NewsTool()
    print(tool.execute(query="Mumbai travel delay"))
