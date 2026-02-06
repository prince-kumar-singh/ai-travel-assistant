import feedparser
from typing import Dict, Any
from tools.base_tool import BaseTool

class RSSTool(BaseTool):
    """
    Fallback tool to fetch news from RSS feeds when the main News API fails.
    """
    def __init__(self):
        self.feeds = {
            "google_news": "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en",
            "bbc_world": "http://feeds.bbci.co.uk/news/world/rss.xml"
        }

    def execute(self, query: str = "travel safety", **kwargs) -> Dict[str, Any]:
        """
        Fetch news from RSS feeds.
        
        Args:
            query (str): Search query for Google News RSS.
            
        Returns:
            Dict: List of news items.
        """
        try:
            # Prioritize Google News with specific query
            feed_url = self.feeds["google_news"].format(query=query)
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                return {"error": f"Error parsing RSS feed: {feed.bozo_exception}"}
                
            results = []
            for entry in feed.entries[:5]:
                results.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "N/A"),
                    "summary": entry.get("summary", "No summary available")
                })
                
            return {
                "status": "success",
                "source": "RSS_Fallback",
                "articles": results
            }
            
        except Exception as e:
            return {"error": f"RSS Tool execution failed: {e}"}

if __name__ == "__main__":
    tool = RSSTool()
    print(tool.execute(query="Bangalore traffic"))
