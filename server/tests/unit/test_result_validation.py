import pytest
from unittest.mock import Mock
from src.services.result_processor import ResultProcessor
from src.models.search_metadata import SearchMetadata


class TestResultProcessor:
    
    def setup_method(self):
        self.service = ResultProcessor()
    
    def test_validate_metadata_success(self):
        # Arrange
        metadata = SearchMetadata(
            source_url="https://example.com",
            source_file_path="/docs/example.md",
            title="Example Title",
            source_domain="example.com",
            chunk_index=1,
            content_type="article",
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.validate_metadata(metadata)
        
        # Assert
        assert result["success"] is True
        assert result["message"] == "Metadata validation passed"
    
    def test_validate_metadata_invalid_url(self):
        # Arrange
        metadata = SearchMetadata(
            source_url="invalid-url",
            source_file_path="/docs/example.md",
            title="Example Title",
            source_domain="example.com",
            chunk_index=1,
            content_type="article",
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.validate_metadata(metadata)
        
        # Assert
        assert result["success"] is False
        assert "Invalid source URL" in result["message"]
    
    def test_validate_metadata_missing_file_path(self):
        # Arrange
        metadata = SearchMetadata(
            source_url="https://example.com",
            source_file_path="",
            title="Example Title",
            source_domain="example.com",
            chunk_index=1,
            content_type="article",
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.validate_metadata(metadata)
        
        # Assert
        assert result["success"] is False
        assert "Source file path is required" in result["message"]
    
    def test_validate_metadata_missing_title(self):
        # Arrange
        metadata = SearchMetadata(
            source_url="https://example.com",
            source_file_path="/docs/example.md",
            title="",
            source_domain="example.com",
            chunk_index=1,
            content_type="article",
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.validate_metadata(metadata)
        
        # Assert
        assert result["success"] is False
        assert "Title is required" in result["message"]
    
    def test_validate_metadata_missing_domain(self):
        # Arrange
        metadata = SearchMetadata(
            source_url="https://example.com",
            source_file_path="/docs/example.md",
            title="Example Title",
            source_domain="",
            chunk_index=1,
            content_type="article",
            tags=["test", "example"]
        )
        
        # Act
        result = self.service.validate_metadata(metadata)
        
        # Assert
        assert result["success"] is False
        assert "Source domain is required" in result["message"]
    
    def test_process_results_success(self):
        # Arrange
        search_results = [
            {
                "payload": {
                    "content": "Test content",
                    "url": "https://example.com",
                    "title": "Test Title",
                    "source_domain": "example.com",
                    "chunk_index": 1,
                    "content_type": "article",
                    "tags": ["test", "example"],
                    "file_path": "/docs/test.md"
                },
                "score": 0.85,
                "search_time_ms": 120.5
            }
        ]
        
        query_id = "test-query-id"
        
        # Act
        result = self.service.process_results(search_results, query_id)
        
        # Assert
        assert result["success"] is True
        assert "Processed 1 retrieved chunks" in result["message"]
        
        data = result["data"]
        assert data.query_id == query_id
        assert len(data.chunks) == 1
        assert data.chunks[0].content == "Test content"
        assert data.chunks[0].score == 0.85
        assert data.chunks[0].source_url == "https://example.com"
        assert data.total_chunks_found == 1
    
    def test_calculate_relevance_scores(self):
        # Arrange
        from src.models.retrieved_chunk import RetrievedChunk
        from src.utils.helpers import generate_uuid
        
        chunks = [
            RetrievedChunk(
                id=generate_uuid(),
                content="Test content",
                score=0.85,
                source_url="https://example.com",
                source_file_path="/docs/test.md",
                chunk_index=1
            )
        ]
        
        # Act
        result = self.service.calculate_relevance_scores(chunks)
        
        # Assert
        assert len(result) == 1
        assert result[0].score == 0.85
    
    def test_validate_retrieval_result_success(self):
        # Arrange
        from src.models.retrieved_chunk import RetrievedChunk
        from src.models.retrieval_result import RetrievalResult
        from src.utils.helpers import generate_uuid
        
        chunks = [
            RetrievedChunk(
                id=generate_uuid(),
                content="Test content",
                score=0.85,
                source_url="https://example.com",
                source_file_path="/docs/test.md",
                chunk_index=1,
                metadata={
                    "source_url": "https://example.com",
                    "source_file_path": "/docs/test.md",
                    "title": "Test Title",
                    "source_domain": "example.com",
                    "chunk_index": 1,
                    "content_type": "article",
                    "tags": ["test", "example"]
                }
            )
        ]
        
        retrieval_result = RetrievalResult(
            query_id="test-query-id",
            chunks=chunks,
            total_chunks_found=1,
            search_time_ms=120.5
        )
        
        # Act
        result = self.service.validate_retrieval_result(retrieval_result)
        
        # Assert
        assert result["success"] is True
        assert result["message"] == "Retrieval result validation passed"