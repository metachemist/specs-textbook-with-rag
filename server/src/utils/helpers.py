import uuid
from datetime import datetime
from typing import Union


def generate_uuid() -> str:
    """
    Generate a UUID string.
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """
    Get the current timestamp.
    
    Returns:
        Current datetime object
    """
    return datetime.now()


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text
    """
    return ' '.join(text.split())


def calculate_word_count(text: str) -> int:
    """
    Calculate the word count of a text.
    
    Args:
        text: Input text
        
    Returns:
        Number of words in the text
    """
    return len(text.split())


def calculate_character_count(text: str) -> int:
    """
    Calculate the character count of a text (excluding whitespace).
    
    Args:
        text: Input text
        
    Returns:
        Number of characters in the text (excluding whitespace)
    """
    return len(text.replace(' ', ''))