import pytest
from src.services.text_cleaning_service import TextCleaningService
from src.models.url_content import URLContent
from src.utils.helpers import get_current_timestamp


class TestTextCleaningService:
    
    def setup_method(self):
        self.service = TextCleaningService()
    
    def test_clean_html_content_success(self):
        # Arrange
        html_content = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Header</h1>
                <p>This is a <strong>paragraph</strong> with some text.</p>
                <script>alert('test');</script>
                <style>body { color: red; }</style>
                <p>Another paragraph.</p>
            </body>
        </html>
        """
        url_content = URLContent(
            id="test-id",
            url="https://example.com",
            raw_content=html_content,
            status_code=200,
            fetched_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.clean_html_content(url_content)
        
        # Assert
        assert result["success"] is True
        assert "Header" in result["data"].clean_content
        assert "This is a paragraph with some text." in result["data"].clean_content
        assert "Another paragraph." in result["data"].clean_content
        assert "alert" not in result["data"].clean_content  # Script removed
        assert "color: red" not in result["data"].clean_content  # Style removed
        assert result["data"].word_count > 0
        assert result["data"].character_count > 0
        assert result["data"].original_url == "https://example.com"
        assert "HTML tags and scripts removed" in result["data"].processing_notes
    
    def test_clean_html_content_empty(self):
        # Arrange
        url_content = URLContent(
            id="test-id",
            url="https://example.com",
            raw_content="",
            status_code=200,
            fetched_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.clean_html_content(url_content)
        
        # Assert
        assert result["success"] is True
        assert result["data"].clean_content == ""
        assert result["data"].word_count == 0
        assert result["data"].character_count == 0
    
    def test_clean_html_content_with_special_characters(self):
        # Arrange
        html_content = """
        <html>
            <body>
                <p>Text with special characters: àáâãäåæçèéêë</p>
            </body>
        </html>
        """
        url_content = URLContent(
            id="test-id",
            url="https://example.com",
            raw_content=html_content,
            status_code=200,
            fetched_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.clean_html_content(url_content)
        
        # Assert
        assert result["success"] is True
        assert "àáâãäåæçèéêë" in result["data"].clean_content
    
    def test_clean_content_with_encoding_handling(self):
        # Arrange
        html_content = """
        <html>
            <body>
                <p>Test content with encoding</p>
            </body>
        </html>
        """
        url_content = URLContent(
            id="test-id",
            url="https://example.com",
            raw_content=html_content,
            status_code=200,
            encoding="utf-8",
            fetched_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.clean_content_with_encoding_handling(url_content)
        
        # Assert
        assert result["success"] is True
        assert "Test content with encoding" in result["data"].clean_content
    
    def test_clean_html_content_with_code_blocks(self):
        # Arrange
        html_content = """
        <html>
            <body>
                <p>Regular text.</p>
                <pre><code>def hello():
    print("Hello, World!")
</code></pre>
                <p>More text.</p>
            </body>
        </html>
        """
        url_content = URLContent(
            id="test-id",
            url="https://example.com",
            raw_content=html_content,
            status_code=200,
            fetched_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.clean_html_content(url_content)
        
        # Assert
        assert result["success"] is True
        assert "def hello" in result["data"].clean_content
        assert 'print("Hello, World!")' in result["data"].clean_content
        assert "Regular text." in result["data"].clean_content
        assert "More text." in result["data"].clean_content