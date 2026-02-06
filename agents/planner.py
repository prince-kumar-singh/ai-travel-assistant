import json
from datetime import datetime
from llm.llm_client import LLMClient
from agents.schemas import Plan
import dateparser

class PlannerAgent:
    """
    Agent responsible for breaking down a user query into a structured plan.
    """
    def __init__(self):
        self.llm = LLMClient()

    def extract_date(self, user_query: str, llm_suggested_date: str = None) -> str:
        """
        Extract and normalize date from user query using dateparser.
        
        Args:
            user_query (str): The user's travel question
            llm_suggested_date (str): Date suggested by LLM (optional)
            
        Returns:
            str: Normalized date in YYYY-MM-DD format or 'Today'/'Tomorrow'
        """
        # Try to parse date from the query using dateparser
        parsed_date = dateparser.parse(
            user_query,
            settings={
                'PREFER_DATES_FROM': 'future',
                'RELATIVE_BASE': datetime.now()
            }
        )
        
        if parsed_date:
            formatted_date = parsed_date.strftime('%Y-%m-%d')
            
            # Check if it's today or tomorrow for friendly display
            today = datetime.now().date()
            if parsed_date.date() == today:
                return "Today"
            elif (parsed_date.date() - today).days == 1:
                return "Tomorrow"
            else:
                return formatted_date
        
        # Fallback to LLM suggested date or 'Today'
        return llm_suggested_date if llm_suggested_date else "Today"

    def plan(self, user_query: str) -> dict:
        """
        Generates a plan based on the user query with Pydantic validation.
        
        Args:
            user_query (str): The user's travel question.
            
        Returns:
            dict: The validated JSON plan.
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
            plan_dict = json.loads(cleaned_response)
            
            # Extract and normalize date using dateparser
            llm_date = plan_dict.get("date", "Today")
            normalized_date = self.extract_date(user_query, llm_date)
            plan_dict["date"] = normalized_date
            
            # Validate with Pydantic
            validated_plan = Plan(**plan_dict)
            return validated_plan.dict()
            
        except json.JSONDecodeError as e:
            print(f"[Planner] Error parsing plan JSON: {e}. Raw output: {response_text}")
            return {"error": "Failed to generate valid plan - JSON parsing error"}
        except Exception as e:
            print(f"[Planner] Validation error: {e}")
            return {"error": f"Plan validation failed: {str(e)}"}

if __name__ == "__main__":
    planner = PlannerAgent()
    print(planner.plan("Is it safe to go to Paris next week?"))
