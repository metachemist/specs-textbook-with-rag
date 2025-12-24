import re
from urllib.parse import urlparse
from typing import Union


def is_valid_url(url: str) -> bool:
    """
    Validate if the given string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        # Check if both scheme and netloc are present
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_valid_http_url(url: str) -> bool:
    """
    Validate if the given string is a valid HTTP or HTTPS URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if the URL is a valid HTTP/HTTPS URL, False otherwise
    """
    if not is_valid_url(url):
        return False
    
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https']
    except Exception:
        return False


def extract_domain(url: str) -> str:
    """
    Extract the domain from a URL.
    
    Args:
        url: URL string
        
    Returns:
        Domain string
    """
    try:
        result = urlparse(url)
        return result.netloc
    except Exception:
        return ""