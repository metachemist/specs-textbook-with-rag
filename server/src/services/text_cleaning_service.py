from bs4 import BeautifulSoup
from typing import Dict, Any
from src.services.base_service import BaseService
from src.models.clean_text import CleanText
from src.models.url_content import URLContent
from src.utils.helpers import generate_uuid, get_current_timestamp, calculate_word_count, calculate_character_count
from src.config.settings import settings


class TextCleaningService(BaseService):
    """
    Service for cleaning and processing raw HTML content into clean text
    """
    
    def __init__(self):
        super().__init__("TextCleaningService")
    
    def clean_html_content(self, url_content: URLContent) -> Dict[str, Any]:
        """
        Clean raw HTML content to extract meaningful text while removing markup
        
        Args:
            url_content: URLContent model with raw HTML content
            
        Returns:
            Dictionary with success status and either clean text or error
        """
        try:
            # Parse the HTML content
            soup = BeautifulSoup(url_content.raw_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text preserving paragraph structure
            text_parts = []
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div', 'span', 'pre', 'code']):
                text = element.get_text(separator=' ', strip=True)
                if text:
                    text_parts.append(text)
            
            # Join the text parts
            clean_text_content = ' '.join(text_parts)
            
            # Normalize the text (remove extra whitespace)
            clean_text_content = ' '.join(clean_text_content.split())
            
            # Create CleanText model instance
            clean_text = CleanText(
                id=url_content.id,  # Using the same ID as the URLContent for the relationship
                clean_content=clean_text_content,
                original_url=url_content.url,
                word_count=calculate_word_count(clean_text_content),
                character_count=calculate_character_count(clean_text_content),
                cleaned_at=get_current_timestamp(),
                processing_notes="HTML tags and scripts removed, text normalized"
            )
            
            return self.handle_success(data=clean_text, message="Content cleaned successfully")
        
        except Exception as e:
            return self.handle_error(e, "clean_html_content")
    
    def clean_content_with_encoding_handling(self, url_content: URLContent) -> Dict[str, Any]:
        """
        Clean content with special handling for different encodings and special characters
        
        Args:
            url_content: URLContent model with raw content
            
        Returns:
            Dictionary with success status and either clean text or error
        """
        try:
            # If encoding is specified in URLContent, try to handle it
            raw_content = url_content.raw_content
            
            # Handle common encoding issues
            if url_content.encoding:
                try:
                    # If the content is bytes, decode it
                    if isinstance(raw_content, bytes):
                        raw_content = raw_content.decode(url_content.encoding)
                except (UnicodeDecodeError, LookupError):
                    # If specified encoding fails, try default
                    try:
                        raw_content = raw_content.decode('utf-8')
                    except (UnicodeDecodeError, AttributeError):
                        # If that fails too, try latin-1 which handles most characters
                        raw_content = raw_content.decode('latin-1', errors='ignore')
            
            # Update the url_content with properly decoded content
            url_content.raw_content = raw_content
            
            # Now clean the HTML content
            return self.clean_html_content(url_content)
        
        except Exception as e:
            return self.handle_error(e, "clean_content_with_encoding_handling")