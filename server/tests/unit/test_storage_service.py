import pytest
from unittest.mock import Mock, patch
from src.services.storage_service import StorageService
from src.models.embedding import Embedding
from src.models.metadata import Metadata
from src.utils.helpers import get_current_timestamp


class TestStorageService:
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    def setup_method(self, mock_get_client):
        # Mock the Qdrant client
        self.mock_qdrant_client = Mock()
        mock_get_client.return_value = self.mock_qdrant_client
        self.service = StorageService()
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    @patch('src.services.storage_service.qdrant_config.collection_exists')
    def test_store_embeddings_success(self, mock_collection_exists, mock_get_client):
        # Arrange
        mock_collection_exists.return_value = True
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        embeddings = [
            Embedding(
                id="embedding-1",
                vector=[0.1, 0.2, 0.3],
                model="embed-english-v3.0",
                created_at=get_current_timestamp()
            )
        ]
        
        metadata_list = [
            Metadata(
                url="https://example.com",
                title="Example Title",
                source_domain="example.com",
                chunk_index=0,
                content_type="article",
                created_at=get_current_timestamp(),
                tags=["test", "example"]
            )
        ]
        
        # Act
        result = self.service.store_embeddings(embeddings, metadata_list)
        
        # Assert
        assert result["success"] is True
        assert "Successfully stored 1 embeddings" in result["message"]
        mock_client.upsert.assert_called_once()
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    @patch('src.services.storage_service.qdrant_config.collection_exists')
    def test_store_single_embedding_success(self, mock_collection_exists, mock_get_client):
        # Arrange
        mock_collection_exists.return_value = True
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        embedding = Embedding(
            id="embedding-1",
            vector=[0.1, 0.2, 0.3],
            model="embed-english-v3.0",
            created_at=get_current_timestamp()
        )
        
        metadata = Metadata(
            url="https://example.com",
            title="Example Title",
            source_domain="example.com",
            chunk_index=0,
            content_type="article",
            created_at=get_current_timestamp(),
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.store_single_embedding(embedding, metadata)
        
        # Assert
        assert result["success"] is True
        assert "Successfully stored embedding" in result["message"]
        mock_client.upsert.assert_called_once()
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    @patch('src.services.storage_service.qdrant_config.collection_exists')
    def test_store_embeddings_collection_not_exists(self, mock_collection_exists, mock_get_client):
        # Arrange
        mock_collection_exists.return_value = False
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Mock the create_collection method
        with patch('src.services.storage_service.qdrant_config.create_collection') as mock_create:
            mock_create.return_value = True
            
            embeddings = [
                Embedding(
                    id="embedding-1",
                    vector=[0.1, 0.2, 0.3],
                    model="embed-english-v3.0",
                    created_at=get_current_timestamp()
                )
            ]
            
            metadata_list = [
                Metadata(
                    url="https://example.com",
                    title="Example Title",
                    source_domain="example.com",
                    chunk_index=0,
                    content_type="article",
                    created_at=get_current_timestamp(),
                    tags=["test", "example"]
                )
            ]
            
            # Act
            result = self.service.store_embeddings(embeddings, metadata_list)
            
            # Assert
            assert result["success"] is True
            mock_create.assert_called_once()
            mock_client.upsert.assert_called_once()
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    @patch('src.services.storage_service.qdrant_config.collection_exists')
    def test_store_embeddings_error(self, mock_collection_exists, mock_get_client):
        # Arrange
        mock_collection_exists.return_value = True
        mock_client = Mock()
        mock_client.upsert.side_effect = Exception("Storage Error")
        mock_get_client.return_value = mock_client
        
        embeddings = [
            Embedding(
                id="embedding-1",
                vector=[0.1, 0.2, 0.3],
                model="embed-english-v3.0",
                created_at=get_current_timestamp()
            )
        ]
        
        metadata_list = [
            Metadata(
                url="https://example.com",
                title="Example Title",
                source_domain="example.com",
                chunk_index=0,
                content_type="article",
                created_at=get_current_timestamp(),
                tags=["test", "example"]
            )
        ]
        
        # Act
        result = self.service.store_embeddings(embeddings, metadata_list)
        
        # Assert
        assert result["success"] is False
        assert "Storage Error" in result["error"]
    
    def test_check_collection_exists(self):
        # Arrange
        with patch('src.services.storage_service.qdrant_config.collection_exists') as mock_exists:
            mock_exists.return_value = True
            
            # Act
            result = self.service.check_collection_exists()
            
            # Assert
            assert result is True
            mock_exists.assert_called_once()
    
    @patch('src.services.storage_service.qdrant_config.get_client')
    @patch('src.services.storage_service.qdrant_config.collection_exists')
    def test_retrieve_similar(self, mock_collection_exists, mock_get_client):
        # Arrange
        mock_collection_exists.return_value = True
        mock_client = Mock()
        mock_search_result = [
            Mock(id="result-1", score=0.9, payload={"url": "https://example.com"})
        ]
        mock_client.search.return_value = mock_search_result
        mock_get_client.return_value = mock_client
        
        query_vector = [0.1, 0.2, 0.3]
        
        # Act
        result = self.service.retrieve_similar(query_vector, limit=5)
        
        # Assert
        assert result["success"] is True
        assert len(result["data"]) == 1
        assert "Retrieved 1 similar embeddings" in result["message"]
        mock_client.search.assert_called_once()