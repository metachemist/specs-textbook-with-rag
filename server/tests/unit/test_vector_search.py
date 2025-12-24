import pytest
from unittest.mock import Mock, patch
from src.services.qdrant_search_service import QdrantSearchService
from src.models.retrieval_result import RetrievalResult


class TestQdrantSearchService:
    
    @patch('src.services.qdrant_search_service.qdrant_config.get_client')
    def setup_method(self, mock_get_client):
        # Mock the Qdrant client
        self.mock_qdrant_client = Mock()
        mock_get_client.return_value = self.mock_qdrant_client
        self.service = QdrantSearchService()
    
    @patch('src.services.qdrant_search_service.qdrant_config.get_client')
    def test_search_success(self, mock_get_client):
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock search result
        mock_result = Mock()
        mock_result.payload = {
            "content": "Test content",
            "url": "https://example.com",
            "title": "Test Title",
            "source_domain": "example.com",
            "chunk_index": 1,
            "content_type": "article",
            "tags": ["test", "example"],
            "created_at": "2025-12-24T10:00:00Z",
            "file_path": "/docs/test.md"
        }
        mock_result.score = 0.85
        
        mock_client.search.return_value = [mock_result]
        
        query_vector = [0.1, 0.2, 0.3]
        
        # Act
        result = self.service.search(query_vector, top_k=5)
        
        # Assert
        assert result["success"] is True
        assert "Found 1 relevant chunks" in result["message"]
        
        data = result["data"]
        assert isinstance(data, RetrievalResult)
        assert len(data.chunks) == 1
        assert data.chunks[0].content == "Test content"
        assert data.chunks[0].score == 0.85
        assert data.chunks[0].source_url == "https://example.com"
        assert data.total_chunks_found == 1
        
        # Verify that search was called with correct parameters
        mock_client.search.assert_called_once()
        call_args = mock_client.search.call_args
        assert call_args.kwargs["collection_name"] == self.service.collection_name
        assert call_args.kwargs["query_vector"] == query_vector
        assert call_args.kwargs["limit"] == 5
    
    @patch('src.services.qdrant_search_service.qdrant_config.get_client')
    def test_search_with_filters(self, mock_get_client):
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock search result
        mock_result = Mock()
        mock_result.payload = {
            "content": "Filtered content",
            "url": "https://filtered.com",
            "title": "Filtered Title",
            "source_domain": "filtered.com",
            "chunk_index": 1,
            "content_type": "article",
            "tags": ["filtered", "test"],
            "created_at": "2025-12-24T10:00:00Z",
            "file_path": "/docs/filtered.md"
        }
        mock_result.score = 0.92
        
        mock_client.search.return_value = [mock_result]
        
        query_vector = [0.4, 0.5, 0.6]
        
        # Act
        result = self.service.search_with_filters(
            query_vector, 
            top_k=3, 
            content_type="article", 
            source_domain="filtered.com",
            tags=["filtered"]
        )
        
        # Assert
        assert result["success"] is True
        assert "Found 1 relevant chunks" in result["message"]
        
        data = result["data"]
        assert isinstance(data, RetrievalResult)
        assert len(data.chunks) == 1
        assert data.chunks[0].content == "Filtered content"
        assert data.chunks[0].score == 0.92
        
        # Verify that search was called
        mock_client.search.assert_called_once()
    
    @patch('src.services.qdrant_search_service.qdrant_config.get_client')
    def test_search_error(self, mock_get_client):
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_client.search.side_effect = Exception("Search Error")
        
        query_vector = [0.7, 0.8, 0.9]
        
        # Act
        result = self.service.search(query_vector)
        
        # Assert
        assert result["success"] is False
        assert "Search Error" in result["error"]
    
    def test_verify_collection_exists(self):
        # Arrange
        with patch.object(self.service.client, 'get_collection') as mock_get_collection:
            mock_get_collection.return_value = True
            
            # Act
            result = self.service.verify_collection_exists()
            
            # Assert
            assert result is True
            mock_get_collection.assert_called_once_with(self.service.collection_name)
        
        # Test when collection doesn't exist
        with patch.object(self.service.client, 'get_collection') as mock_get_collection:
            mock_get_collection.side_effect = Exception("Collection not found")
            
            # Act
            result = self.service.verify_collection_exists()
            
            # Assert
            assert result is False
            mock_get_collection.assert_called_once_with(self.service.collection_name)