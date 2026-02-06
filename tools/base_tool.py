from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    """Abstract base class for all tools."""

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool action.
        
        Args:
            **kwargs: dynamic arguments required by the specific tool.
            
        Returns:
            Dict[str, Any]: The result of the tool execution.
        """
        pass
