import json
from llm.llm_client import LLMClient

class PlannerAgent:
    """
    Agent responsible for breaking down a user query into a structured plan.
    """
    def __init__(self):
        self.llm = LLMClient()

    def plan(self, user_query: str) -> dict:
        """
        Generates a plan based on the user query.
        
        Args:
            user_query (str): The user's travel question.
            
        Returns:
            dict: The JSON plan.
        """
        prompt = f"""
        You are a Planner Agent for a Travel Safety Assistant.
        Your goal is to create a step-by-step plan to answer the user's travel safety question.
        
        Available Tools:
        1. WeatherTool: Fetch weather data. Args: "city"
        2. NewsTool: Fetch news/alerts. Args: "query"
        
        User Query: "{user_query}"
        
        Return STRICT JSON format ONLY. Do not include markdown formatting (```json ... ```).
        The JSON structure must be:
        {{
            "destination": "Extracted City Name",
            "date": "Extracted Date (YYYY-MM-DD) or 'Tomorrow'/'Today'",
            "steps": [
                {{
                    "action": "fetch_weather",
                    "tool": "WeatherTool",
                    "args": {{ "city": "City Name" }}
                }},
                {{
                    "action": "fetch_news",
                    "tool": "NewsTool",
                    "args": {{ "query": "City Name travel safety OR strike OR protest" }}
                }}
            ]
        }}
        """
        
        response_text = self.llm.generate(prompt)
        
        # Clean up potential markdown formatting
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            plan = json.loads(cleaned_response)
            return plan
        except json.JSONDecodeError:
            # Fallback simple plan if LLM fails to generate valid JSON
            print(f"Error parsing plan JSON. Raw output: {response_text}")
            return {
                "error": "Failed to generate valid plan"
            }

if __name__ == "__main__":
    planner = PlannerAgent()
    print(planner.plan("Is it safe to go to Paris next week?"))
