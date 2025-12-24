import logging
import sys
from typing import Optional
from src.config.settings import settings


def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and log level.
    
    Args:
        name: Name of the logger
        log_level: Optional log level, defaults to settings.log_level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Set log level
    level = log_level or settings.log_level
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    return setup_logger(name)