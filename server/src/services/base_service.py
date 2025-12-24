from abc import ABC
from typing import Any, Dict, Optional
from src.utils.logger import get_logger


class BaseService(ABC):
    """
    Base service class that provides common functionality for all services
    """
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
        self.name = name
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Standardized error handling for all services
        """
        error_msg = f"Error in {self.name} {context}: {str(error)}"
        self.logger.error(error_msg)
        
        return {
            "success": False,
            "error": str(error),
            "message": error_msg
        }
    
    def handle_success(self, data: Optional[Any] = None, message: str = "") -> Dict[str, Any]:
        """
        Standardized success response for all services
        """
        result = {
            "success": True,
            "message": message
        }
        
        if data is not None:
            result["data"] = data
            
        return result