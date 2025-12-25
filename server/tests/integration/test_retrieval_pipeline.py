import pytest
from unittest.mock import Mock, patch
from rag_service import get_embedding, search_knowledge_base


class TestRetrievalPipeline:
    
    @patch('rag_service.CohereClientWrapper')
    @patch('rag_service.QdrantSearchService')
    @patch('rag_service.ResultProcessor')
    def test_get_embedding_success(self, mock_result_processor, mock_qdrant_service, mock_cohere_client):
        # Arrange
        mock_cohere_wrapper_instance = Mock()
        mock_cohere_client.return_value = mock_cohere_wrapper_instance
        
        mock_embedding_result = Mock()
        mock_embedding_result.success = True
        mock_embedding_result.data = Mock(vector=[0.1, 0.2, 0.3])
        mock_cohere_wrapper_instance.get_embedding.return_value = mock_embedding_result
        
        text = "Test query for embedding"
        
        # Act
        result = get_embedding(text)
        
        # Assert
        assert result["success"] is True
        assert result["data"] == mock_embedding_result.data
        mock_cohere_wrapper_instance.get_embedding.assert_called_once_with(text)
    
    @patch('rag_service.get_embedding')
    @patch('rag_service.QdrantSearchService')
    @patch('rag_service.ResultProcessor')
    def test_search_knowledge_base_success(self, mock_result_processor, mock_qdrant_service, mock_get_embedding):
        # Arrange
        # Mock the embedding result
        mock_get_embedding.return_value = {
            "success": True,
            "data": Mock(vector=[0.1, 0.2, 0.3])
        }
        
        # Mock the Qdrant service
        mock_qdrant_instance = Mock()
        mock_qdrant_service.return_value = mock_qdrant_instance
        
        mock_search_result = Mock()
        mock_search_result.success = True
        mock_search_result.data = Mock(chunks=[])
        mock_qdrant_instance.search.return_value = mock_search_result
        
        # Mock the result processor
        mock_processor_instance = Mock()
        mock_result_processor.return_value = mock_processor_instance
        
        mock_process_result = Mock()
        mock_process_result.success = True
        mock_process_result.data = Mock(chunks=[])
        mock_processor_instance.process_results.return_value = mock_process_result
        
        query_text = "What is a node?"
        
        # Act
        result = search_knowledge_base(query_text)
        
        # Assert
        assert result["success"] is True
        mock_get_embedding.assert_called_once_with(query_text)
        mock_qdrant_instance.search.assert_called_once()
        mock_processor_instance.process_results.assert_called_once()
    
    @patch('rag_service.get_embedding')
    def test_search_knowledge_base_embedding_failure(self, mock_get_embedding):
        # Arrange
        mock_get_embedding.return_value = {
            "success": False,
            "error": "Embedding failed"
        }
        
        query_text = "What is a node?"
        
        # Act
        result = search_knowledge_base(query_text)
        
        # Assert
        assert result["success"] is False
        assert "Embedding failed" in result["error"]
    
    @patch('rag_service.get_embedding')
    @patch('rag_service.QdrantSearchService')
    def test_search_knowledge_base_search_failure(self, mock_qdrant_service, mock_get_embedding):
        # Arrange
        # Mock the embedding result
        mock_get_embedding.return_value = {
            "success": True,
            "data": Mock(vector=[0.1, 0.2, 0.3])
        }
        
        # Mock the Qdrant service to return failure
        mock_qdrant_instance = Mock()
        mock_qdrant_service.return_value = mock_qdrant_instance
        
        mock_search_result = Mock()
        mock_search_result.success = False
        mock_search_result.error = "Search failed"
        mock_qdrant_instance.search.return_value = mock_search_result
        
        query_text = "What is a node?"
        
        # Act
        result = search_knowledge_base(query_text)
        
        # Assert
        assert result["success"] is False
        assert "Search failed" in result["error"]
    
    @patch('rag_service.CohereClientWrapper')
    def test_get_embedding_environment_error(self, mock_cohere_client):
        # Arrange
        # This test would require mocking the environment variables
        # to simulate missing environment variables
        pass