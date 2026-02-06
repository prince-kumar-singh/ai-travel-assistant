from typing import Dict, Any, List
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool

class ExecutorAgent:
    """
    Agent responsible for executing the steps in the plan.
    """
    def __init__(self):
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()
        self.tools = {
            "WeatherTool": self.weather_tool,
            "NewsTool": self.news_tool
        }

    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the given plan.
        
        Args:
            plan (Dict): The JSON plan from the Planner.
            
        Returns:
            Dict: The context containing results from tool executions.
        """
        context = {
            "destination": plan.get("destination"),
            "date": plan.get("date"),
            "results": {}
        }
        
        if "error" in plan:
            return {"error": plan["error"]}
            
        steps = plan.get("steps", [])
        print(f"\n[Executor] Executing {len(steps)} steps for {context['destination']}...")
        
        for step in steps:
            tool_name = step.get("tool")
            action = step.get("action")
            args = step.get("args", {})
            
            if tool_name in self.tools:
                print(f"[Executor] Running {tool_name} with args: {args}")
                tool = self.tools[tool_name]
                try:
                    result = tool.execute(**args)
                    context["results"][action] = result
                except Exception as e:
                    print(f"[Executor] Error running {tool_name}: {e}")
                    context["results"][action] = {"error": str(e)}
            else:
                print(f"[Executor] Unknown tool: {tool_name}")
                
        return context
