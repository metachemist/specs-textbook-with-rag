import pytest
from unittest.mock import Mock, patch
from src.services.ingestion_pipeline import IngestionPipeline


class TestIngestionPipeline:
    
    @patch('src.services.ingestion_pipeline.URLFetchService')
    @patch('src.services.ingestion_pipeline.TextCleaningService')
    @patch('src.services.ingestion_pipeline.ChunkingService')
    @patch('src.services.ingestion_pipeline.EmbeddingService')
    @patch('src.services.ingestion_pipeline.StorageService')
    def setup_method(self, mock_storage, mock_embedding, mock_chunking, mock_cleaning, mock_fetch):
        # Create mock services
        self.mock_fetch_service = Mock()
        self.mock_cleaning_service = Mock()
        self.mock_chunking_service = Mock()
        self.mock_embedding_service = Mock()
        self.mock_storage_service = Mock()
        
        # Patch the services in the pipeline
        with patch('src.services.ingestion_pipeline.URLFetchService') as mock_fetch_cls, \
             patch('src.services.ingestion_pipeline.TextCleaningService') as mock_cleaning_cls, \
             patch('src.services.ingestion_pipeline.ChunkingService') as mock_chunking_cls, \
             patch('src.services.ingestion_pipeline.EmbeddingService') as mock_embedding_cls, \
             patch('src.services.ingestion_pipeline.StorageService') as mock_storage_cls:
            
            mock_fetch_cls.return_value = self.mock_fetch_service
            mock_cleaning_cls.return_value = self.mock_cleaning_service
            mock_chunking_cls.return_value = self.mock_chunking_service
            mock_embedding_cls.return_value = self.mock_embedding_service
            mock_storage_cls.return_value = self.mock_storage_service
            
            self.pipeline = IngestionPipeline()
    
    @patch('src.services.ingestion_pipeline.URLFetchService')
    @patch('src.services.ingestion_pipeline.TextCleaningService')
    @patch('src.services.ingestion_pipeline.ChunkingService')
    @patch('src.services.ingestion_pipeline.EmbeddingService')
    @patch('src.services.ingestion_pipeline.StorageService')
    def test_run_pipeline_success(self, mock_storage, mock_embedding, mock_chunking, mock_cleaning, mock_fetch):
        # Arrange
        mock_fetch_instance = Mock()
        mock_cleaning_instance = Mock()
        mock_chunking_instance = Mock()
        mock_embedding_instance = Mock()
        mock_storage_instance = Mock()
        
        mock_fetch.return_value = mock_fetch_instance
        mock_cleaning.return_value = mock_cleaning_instance
        mock_chunking.return_value = mock_chunking_instance
        mock_embedding.return_value = mock_embedding_instance
        mock_storage.return_value = mock_storage_instance
        
        # Setup successful return values for each service
        mock_fetch_instance.fetch_content_with_retry.return_value = {
            "success": True,
            "data": Mock(id="test-id", url="https://example.com", raw_content="test content")
        }
        
        mock_cleaning_instance.clean_content_with_encoding_handling.return_value = {
            "success": True,
            "data": Mock(id="test-id", clean_content="clean content", original_url="https://example.com")
        }
        
        mock_chunking_instance.chunk_text.return_value = {
            "success": True,
            "data": [Mock(id="chunk-1", content="chunk content", url="https://example.com", chunk_index=0, token_count=10, hash="hash")]
        }
        
        mock_embedding_instance.batch_generate_embeddings.return_value = {
            "success": True,
            "data": [Mock(id="chunk-1", vector=[0.1, 0.2, 0.3])]
        }
        
        mock_storage_instance.store_embeddings.return_value = {
            "success": True
        }
        
        urls = ["https://example.com"]
        
        # Act
        result = self.pipeline.run_pipeline(urls)
        
        # Assert
        assert result["success"] is True
        assert "completed successfully" in result["message"]
        assert result["data"]["processed_urls"] == 1
        assert result["data"]["successful_chunks"] == 1
        
        # Verify that all services were called
        mock_fetch_instance.fetch_content_with_retry.assert_called_once()
        mock_cleaning_instance.clean_content_with_encoding_handling.assert_called_once()
        mock_chunking_instance.chunk_text.assert_called_once()
        mock_embedding_instance.batch_generate_embeddings.assert_called_once()
        mock_storage_instance.store_embeddings.assert_called_once()
    
    @patch('src.services.ingestion_pipeline.URLFetchService')
    @patch('src.services.ingestion_pipeline.TextCleaningService')
    @patch('src.services.ingestion_pipeline.ChunkingService')
    @patch('src.services.ingestion_pipeline.EmbeddingService')
    @patch('src.services.ingestion_pipeline.StorageService')
    def test_run_pipeline_fetch_failure(self, mock_storage, mock_embedding, mock_chunking, mock_cleaning, mock_fetch):
        # Arrange
        mock_fetch_instance = Mock()
        mock_cleaning_instance = Mock()
        mock_chunking_instance = Mock()
        mock_embedding_instance = Mock()
        mock_storage_instance = Mock()
        
        mock_fetch.return_value = mock_fetch_instance
        mock_cleaning.return_value = mock_cleaning_instance
        mock_chunking.return_value = mock_chunking_instance
        mock_embedding.return_value = mock_embedding_instance
        mock_storage.return_value = mock_storage_instance
        
        # Setup failure return value for fetch service
        mock_fetch_instance.fetch_content_with_retry.return_value = {
            "success": False,
            "error": "Failed to fetch"
        }
        
        urls = ["https://example.com"]
        
        # Act
        result = self.pipeline.run_pipeline(urls)
        
        # Assert
        assert result["success"] is True  # Pipeline should continue with other URLs
        # Even if fetching fails, the pipeline should complete with error tracking
        assert "completed" in result["message"]
    
    @patch('src.services.ingestion_pipeline.URLFetchService')
    @patch('src.services.ingestion_pipeline.TextCleaningService')
    @patch('src.services.ingestion_pipeline.ChunkingService')
    @patch('src.services.ingestion_pipeline.EmbeddingService')
    @patch('src.services.ingestion_pipeline.StorageService')
    def test_run_pipeline_multiple_urls(self, mock_storage, mock_embedding, mock_chunking, mock_cleaning, mock_fetch):
        # Arrange
        mock_fetch_instance = Mock()
        mock_cleaning_instance = Mock()
        mock_chunking_instance = Mock()
        mock_embedding_instance = Mock()
        mock_storage_instance = Mock()
        
        mock_fetch.return_value = mock_fetch_instance
        mock_cleaning.return_value = mock_cleaning_instance
        mock_chunking.return_value = mock_chunking_instance
        mock_embedding.return_value = mock_embedding_instance
        mock_storage.return_value = mock_storage_instance
        
        # Setup successful return values
        mock_fetch_instance.fetch_content_with_retry.return_value = {
            "success": True,
            "data": Mock(id="test-id", url="https://example.com", raw_content="test content")
        }
        
        mock_cleaning_instance.clean_content_with_encoding_handling.return_value = {
            "success": True,
            "data": Mock(id="test-id", clean_content="clean content", original_url="https://example.com")
        }
        
        mock_chunking_instance.chunk_text.return_value = {
            "success": True,
            "data": [Mock(id="chunk-1", content="chunk content", url="https://example.com", chunk_index=0, token_count=10, hash="hash")]
        }
        
        mock_embedding_instance.batch_generate_embeddings.return_value = {
            "success": True,
            "data": [Mock(id="chunk-1", vector=[0.1, 0.2, 0.3])]
        }
        
        mock_storage_instance.store_embeddings.return_value = {
            "success": True
        }
        
        urls = ["https://example.com", "https://example2.com"]
        
        # Act
        result = self.pipeline.run_pipeline(urls)
        
        # Assert
        assert result["success"] is True
        assert "completed successfully" in result["message"]
        # The fetch method should be called for each URL
        assert mock_fetch_instance.fetch_content_with_retry.call_count == 2