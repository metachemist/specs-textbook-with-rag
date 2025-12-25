import pytest
from unittest.mock import Mock, patch
from src.services.url_fetch_service import URLFetchService
from src.config.settings import settings


class TestURLFetchService:
    
    def setup_method(self):
        self.service = URLFetchService()
    
    @patch('src.services.url_fetch_service.requests.Session.get')
    def test_fetch_content_success(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.text = "Sample content"
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.encoding = 'utf-8'
        mock_response.reason = 'OK'
        
        mock_get.return_value = mock_response
        url = "https://example.com"
        
        # Act
        result = self.service.fetch_content(url)
        
        # Assert
        assert result["success"] is True
        assert result["data"].url == url
        assert result["data"].raw_content == "Sample content"
        assert result["data"].status_code == 200
        assert result["message"] == "Content fetched successfully"
    
    @patch('src.services.url_fetch_service.requests.Session.get')
    def test_fetch_content_with_error_status(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.text = "Error content"
        mock_response.status_code = 404
        mock_response.headers = {'content-type': 'text/html'}
        mock_response.encoding = 'utf-8'
        mock_response.reason = 'Not Found'
        
        mock_get.return_value = mock_response
        url = "https://example.com/nonexistent"
        
        # Act
        result = self.service.fetch_content(url)
        
        # Assert
        assert result["success"] is True  # Request was made successfully, even if page not found
        assert result["data"].status_code == 404
        assert result["data"].error_message == "HTTP 404: Not Found"
    
    def test_fetch_content_invalid_url(self):
        # Arrange
        invalid_url = "not-a-valid-url"
        
        # Act
        result = self.service.fetch_content(invalid_url)
        
        # Assert
        assert result["success"] is False
        assert "Invalid URL" in result["error"]
    
    @patch('src.services.url_fetch_service.requests.Session.get')
    def test_fetch_content_timeout(self, mock_get):
        # Arrange
        mock_get.side_effect = TimeoutError("Request timeout")
        url = "https://example.com"
        
        # Act
        result = self.service.fetch_content(url)
        
        # Assert
        assert result["success"] is False
        assert "timeout" in result["error"].lower()
    
    @patch('src.services.url_fetch_service.requests.Session.get')
    def test_fetch_content_connection_error(self, mock_get):
        # Arrange
        mock_get.side_effect = ConnectionError("Connection failed")
        url = "https://example.com"
        
        # Act
        result = self.service.fetch_content(url)
        
        # Assert
        assert result["success"] is False
        assert "connection" in result["error"].lower()
    
    @patch('src.services.url_fetch_service.URLFetchService.fetch_content')
    def test_fetch_content_with_retry_success_on_second_attempt(self, mock_fetch_content):
        # Arrange
        mock_fetch_content.side_effect = [
            {"success": False, "error": "First attempt failed"},
            {"success": True, "data": "Success content", "message": "Success"}
        ]
        url = "https://example.com"
        
        # Act
        result = self.service.fetch_content_with_retry(url, max_retries=2)
        
        # Assert
        assert result["success"] is True
        assert mock_fetch_content.call_count == 2  # Called twice (first failed, second succeeded)
    
    @patch('src.services.url_fetch_service.URLFetchService.fetch_content')
    def test_fetch_content_with_retry_all_attempts_fail(self, mock_fetch_content):
        # Arrange
        mock_fetch_content.return_value = {"success": False, "error": "Failed attempt"}
        url = "https://example.com"
        
        # Act
        result = self.service.fetch_content_with_retry(url, max_retries=2)
        
        # Assert
        assert result["success"] is False
        assert "all 2 retry attempts failed" in result["error"].lower()
        assert mock_fetch_content.call_count == 3  # Original call + 2 retries