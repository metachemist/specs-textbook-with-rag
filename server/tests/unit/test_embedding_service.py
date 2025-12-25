import pytest
from unittest.mock import Mock, patch
from src.services.embedding_service import EmbeddingService
from src.models.text_chunk import TextChunk
from src.utils.helpers import get_current_timestamp


class TestEmbeddingService:
    
    @patch('src.services.embedding_service.cohere.Client')
    def setup_method(self, mock_client):
        # Mock the Cohere client
        self.mock_cohere_client = Mock()
        mock_client.return_value = self.mock_cohere_client
        self.service = EmbeddingService()
    
    @patch('src.services.embedding_service.cohere.Client')
    def test_generate_embeddings_success(self, mock_client):
        # Arrange
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        mock_client_instance.embed.return_value = mock_response
        
        text_chunks = [
            TextChunk(
                id="chunk-1",
                content="First chunk content",
                url="https://example.com",
                chunk_index=0,
                token_count=10,
                hash="hash1",
                created_at=get_current_timestamp()
            ),
            TextChunk(
                id="chunk-2",
                content="Second chunk content",
                url="https://example.com",
                chunk_index=1,
                token_count=10,
                hash="hash2",
                created_at=get_current_timestamp()
            )
        ]
        
        # Act
        result = self.service.generate_embeddings(text_chunks)
        
        # Assert
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["data"][0].id == "chunk-1"
        assert result["data"][1].id == "chunk-2"
        assert result["data"][0].vector == [0.1, 0.2, 0.3]
        assert result["data"][1].vector == [0.4, 0.5, 0.6]
        assert result["data"][0].model == "embed-english-v3.0"
        assert result["message"] == "Generated embeddings for 2 chunks"
        
        # Verify that embed was called with correct parameters
        mock_client_instance.embed.assert_called_once_with(
            texts=["First chunk content", "Second chunk content"],
            model="embed-english-v3.0",
            input_type="search_document"
        )
    
    @patch('src.services.embedding_service.cohere.Client')
    def test_generate_embeddings_error(self, mock_client):
        # Arrange
        mock_client_instance = Mock()
        mock_client.return_value = mock_client_instance
        
        mock_client_instance.embed.side_effect = Exception("API Error")
        
        text_chunks = [
            TextChunk(
                id="chunk-1",
                content="First chunk content",
                url="https://example.com",
                chunk_index=0,
                token_count=10,
                hash="hash1",
                created_at=get_current_timestamp()
            )
        ]
        
        # Act
        result = self.service.generate_embeddings(text_chunks)
        
        # Assert
        assert result["success"] is False
        assert "API Error" in result["error"]
    
    @patch('src.services.embedding_service.EmbeddingService.generate_embeddings')
    def test_generate_embeddings_with_retry_success_on_second_attempt(self, mock_generate_embeddings):
        # Arrange
        mock_generate_embeddings.side_effect = [
            {"success": False, "error": "First attempt failed"},
            {"success": True, "data": "Success embeddings", "message": "Success"}
        ]
        
        text_chunks = [
            TextChunk(
                id="chunk-1",
                content="First chunk content",
                url="https://example.com",
                chunk_index=0,
                token_count=10,
                hash="hash1",
                created_at=get_current_timestamp()
            )
        ]
        
        # Act
        result = self.service.generate_embeddings_with_retry(text_chunks, max_retries=2)
        
        # Assert
        assert result["success"] is True
        assert result["data"] == "Success embeddings"
        assert mock_generate_embeddings.call_count == 2  # Called twice (first failed, second succeeded)
    
    @patch('src.services.embedding_service.EmbeddingService.generate_embeddings')
    def test_generate_embeddings_with_retry_all_attempts_fail(self, mock_generate_embeddings):
        # Arrange
        mock_generate_embeddings.return_value = {"success": False, "error": "Failed attempt"}
        
        text_chunks = [
            TextChunk(
                id="chunk-1",
                content="First chunk content",
                url="https://example.com",
                chunk_index=0,
                token_count=10,
                hash="hash1",
                created_at=get_current_timestamp()
            )
        ]
        
        # Act
        result = self.service.generate_embeddings_with_retry(text_chunks, max_retries=2)
        
        # Assert
        assert result["success"] is False
        assert "all 2 retry attempts failed" in result["error"].lower()
        assert mock_generate_embeddings.call_count == 3  # Original call + 2 retries
    
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