import pytest
from unittest.mock import Mock, patch
from src.services.cohere_client import CohereClientWrapper
from src.models.query_vector import QueryVector


class TestCohereClientWrapper:
    
    @patch('src.services.cohere_client.cohere.Client')
    def setup_method(self, mock_client):
        # Mock the Cohere client
        self.mock_cohere_client = Mock()
        mock_client.return_value = self.mock_cohere_client
        self.service = CohereClientWrapper()
    
    @patch('src.services.cohere_client.cohere.Client')
    def test_get_embedding_success(self, mock_client):
        # Arrange
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_client_instance.embed.return_value = mock_response
        
        text = "This is a test query"
        
        # Act
        result = self.service.get_embedding(text)
        
        # Assert
        assert result["success"] is True
        assert isinstance(result["data"], QueryVector)
        assert result["data"].vector == [0.1, 0.2, 0.3]
        assert result["data"].model == "embed-english-v3.0"
        assert result["message"] == "Embedding generated successfully"
        
        # Verify that embed was called with correct parameters
        mock_client_instance.embed.assert_called_once_with(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query"
        )
    
    @patch('src.services.cohere_client.cohere.Client')
    def test_get_embedding_error(self, mock_client):
        # Arrange
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_client_instance.embed.side_effect = Exception("API Error")
        
        text = "This is a test query"
        
        # Act
        result = self.service.get_embedding(text)
        
        # Assert
        assert result["success"] is False
        assert "API Error" in result["error"]
    
    @patch('src.services.cohere_client.cohere.Client')
    def test_get_embeddings_batch_success(self, mock_client):
        # Arrange
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_client_instance.embed.return_value = mock_response
        
        texts = ["This is a test query", "Another test query"]
        
        # Act
        result = self.service.get_embeddings_batch(texts)
        
        # Assert
        assert result["success"] is True
        assert result["data"] == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        assert "2 texts successfully" in result["message"]
        
        # Verify that embed was called with correct parameters
        mock_client_instance.embed.assert_called_once_with(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_query"
        )
    
    def test_validate_embedding_model(self):
        # Arrange
        valid_model = "embed-english-v3.0"
        invalid_model = "invalid-model"
        
        # Act
        valid_result = self.service.validate_embedding_model(valid_model)
        invalid_result = self.service.validate_embedding_model(invalid_model)
        
        # Assert
        assert valid_result is True
        assert invalid_result is False