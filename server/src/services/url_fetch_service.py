import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin, urlparse
from src.services.base_service import BaseService
from src.models.url_content import URLContent
from src.utils.validators import is_valid_http_url
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.config.settings import settings


class URLFetchService(BaseService):
    """
    Service for fetching content from URLs
    """
    
    def __init__(self):
        super().__init__("URLFetchService")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_content(self, url: str) -> Dict[str, Any]:
        """
        Fetch content from a given URL with proper error handling
        
        Args:
            url: The URL to fetch content from
            
        Returns:
            Dictionary with success status and either content or error
        """
        # Validate URL first
        if not is_valid_http_url(url):
            return self.handle_error(ValueError(f"Invalid URL: {url}"), "fetch_content")
        
        try:
            response = self.session.get(
                url,
                timeout=settings.request_timeout,
                allow_redirects=True
            )
            
            # Create URLContent model instance
            url_content = URLContent(
                id=generate_uuid(),
                url=url,
                raw_content=response.text,
                status_code=response.status_code,
                content_type=response.headers.get('content-type'),
                fetched_at=get_current_timestamp(),
                encoding=response.encoding
            )
            
            # If status code indicates an error, add error message
            if not (200 <= response.status_code < 300):
                url_content.error_message = f"HTTP {response.status_code}: {response.reason}"
            
            return self.handle_success(data=url_content, message="Content fetched successfully")
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {settings.request_timeout} seconds for URL: {url}"
            return self.handle_error(requests.exceptions.Timeout(error_msg), "fetch_content")
        
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error for URL: {url}"
            return self.handle_error(requests.exceptions.ConnectionError(error_msg), "fetch_content")
        
        except requests.exceptions.RequestException as e:
            return self.handle_error(e, "fetch_content")
        
        except Exception as e:
            return self.handle_error(e, "fetch_content")
    
    def fetch_content_with_retry(self, url: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Fetch content with retry mechanism for transient failures
        
        Args:
            url: The URL to fetch content from
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary with success status and either content or error
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            result = self.fetch_content(url)
            
            # If successful, return immediately
            if result["success"]:
                return result
            
            # If it's the last attempt, break and return the error
            if attempt == max_retries:
                break
            
            # Log the retry attempt
            self.logger.warning(f"Attempt {attempt + 1} failed for {url}, retrying...")
            last_error = result["error"]
        
        # If we exhausted all retries, return the last error
        return self.handle_error(Exception(f"All {max_retries} retry attempts failed. Last error: {last_error}"), "fetch_content_with_retry")