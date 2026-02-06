from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class PlanStep(BaseModel):
    """Schema for a single step in the execution plan."""
    action: str = Field(..., description="Action name (e.g., 'fetch_weather', 'fetch_news')")
    tool: str = Field(..., description="Tool to use (e.g., 'WeatherTool', 'NewsTool')")
    args: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")


class Plan(BaseModel):
    """Schema for the complete plan from Planner Agent."""
    destination: str = Field(..., description="Extracted destination city name")
    date: str = Field(..., description="Extracted date in YYYY-MM-DD format or 'Today'/'Tomorrow'")
    steps: List[PlanStep] = Field(..., description="List of execution steps")

    @validator('steps')
    def validate_steps(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Plan must contain at least one step")
        return v


class WeatherInfo(BaseModel):
    """Schema for weather information."""
    condition: str = Field(..., description="Weather condition description")
    temperature: float = Field(..., description="Temperature in Celsius")


class FinalRecommendation(BaseModel):
    """Schema for the final verification response."""
    destination: str = Field(..., description="Destination city name")
    date: str = Field(..., description="Travel date")
    weather: WeatherInfo = Field(..., description="Weather information")
    alerts: List[str] = Field(default_factory=list, description="Travel safety alerts")
    travel_score: int = Field(..., ge=0, le=10, description="Safety score from 0 (unsafe) to 10 (safe)")
    recommendation: str = Field(..., description="AI-generated travel recommendation")

    @validator('travel_score')
    def validate_score(cls, v):
        if not 0 <= v <= 10:
            raise ValueError("Travel score must be between 0 and 10")
        return v
