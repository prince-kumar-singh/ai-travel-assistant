import json
from typing import Dict, Any
from agents.planner import LLMClient
from tools.rss_tool import RSSTool

class VerifierAgent:
    """
    Agent responsible for validating results and providing the final recommendation.
    Handles fallback to RSS if necessary.
    """
    def __init__(self):
        self.llm = LLMClient()
        self.rss_tool = RSSTool()

    def verify_and_respond(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies the results and generates the final response.
        
        Args:
            context (Dict): The context from the Executor.
            
        Returns:
            Dict: The final structured output.
        """
        results = context.get("results", {})
        destination = context.get("destination", "Unknown")
        
        # Check News Data
        news_data = results.get("fetch_news", {})
        if "error" in news_data or news_data.get("status") != "success":
            print("[Verifier] News API failed or no specific news found. Activating RSS Fallback...")
            # Fallback to RSS
            rss_query = f"{destination} travel safety"
            rss_result = self.rss_tool.execute(query=rss_query)
            results["fetch_news_fallback"] = rss_result
            
        # Synthesize with LLM
        final_prompt = f"""
        You are a Verifier Agent for a Travel Safety Assistant.
        Analyze the gathered data and provide a travel safety assessment.
        
        Destination: {destination}
        Date: {context.get("date")}
        
        Weather Data:
        {json.dumps(results.get("fetch_weather", {}), indent=2)}
        
        News/Alerts Data:
        {json.dumps(results.get("fetch_news", {}), indent=2)}
        
        Fallback RSS Data (if primary news failed):
        {json.dumps(results.get("fetch_news_fallback", {}), indent=2)}
        
        Based on this, return a JSON response (STRICT JSON ONLY, no markdown):
        {{
            "destination": "{destination}",
            "date": "{context.get("date")}",
            "weather": {{
                "condition": "Summarized condition from weather data",
                "temperature": "Temp from weather data"
            }},
            "alerts": ["List of summarized key alerts or 'No major alerts'"],
            "travel_score": 0-10 (10 = Safe, 0 = Unsafe),
            "recommendation": "Short advice based on score and alerts"
        }}
        """
        
        response_text = self.llm.generate(final_prompt)
        
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            final_json = json.loads(cleaned_response)
            return final_json
        except json.JSONDecodeError:
            return {
                "error": "Failed to generate final verification response",
                "raw_output": response_text
            }
