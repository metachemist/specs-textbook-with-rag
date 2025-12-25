import pytest
from src.services.chunking_service import ChunkingService
from src.models.clean_text import CleanText
from src.utils.helpers import get_current_timestamp


class TestChunkingService:
    
    def setup_method(self):
        self.service = ChunkingService()
    
    def test_chunk_text_basic(self):
        # Arrange
        clean_text = CleanText(
            id="test-id",
            clean_content="This is a test sentence. This is another test sentence. And a third one.",
            original_url="https://example.com",
            word_count=12,
            character_count=68,
            cleaned_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.chunk_text(clean_text)
        
        # Assert
        assert result["success"] is True
        assert len(result["data"]) > 0
        assert result["data"][0].content == clean_text.clean_content
        assert result["data"][0].url == clean_text.original_url
        assert result["data"][0].chunk_index == 0
        assert result["data"][0].token_count > 0
        assert len(result["data"][0].hash) > 0  # Hash should be generated
        assert result["message"] == "Text chunked into 1 chunks"
    
    def test_chunk_text_with_paragraphs(self):
        # Arrange
        content = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        clean_text = CleanText(
            id="test-id",
            clean_content=content,
            original_url="https://example.com",
            word_count=9,
            character_count=54,
            cleaned_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.chunk_text(clean_text)
        
        # Assert
        assert result["success"] is True
        assert len(result["data"]) >= 1  # Could be multiple chunks depending on settings
        for i, chunk in enumerate(result["data"]):
            assert chunk.chunk_index == i
            assert chunk.url == clean_text.original_url
            assert len(chunk.content) > 0
            assert len(chunk.hash) > 0
    
    def test_chunk_large_text(self):
        # Arrange
        large_text = "This is a sentence. " * 100  # Create a large text
        clean_text = CleanText(
            id="test-id",
            clean_content=large_text,
            original_url="https://example.com",
            word_count=300,
            character_count=len(large_text),
            cleaned_at=get_current_timestamp()
        )
        
        # Act
        result = self.service.chunk_text(clean_text)
        
        # Assert
        assert result["success"] is True
        assert len(result["data"]) > 1  # Should be split into multiple chunks
        total_content = "".join([chunk.content for chunk in result["data"]])
        # Note: Due to overlapping and splitting, exact match might not be possible
        # but the total should be close to the original
        assert len(total_content) <= len(large_text)
    
    def test_estimate_token_count(self):
        # Arrange
        text = "This is a test sentence."
        
        # Act
        token_count = self.service._estimate_token_count(text)
        
        # Assert
        # The estimation is rough, so we just check it's positive and reasonable
        assert token_count > 0
        assert token_count < len(text)  # Should be less than character count
    
    def test_generate_content_hash(self):
        # Arrange
        content = "This is test content"
        
        # Act
        hash1 = self.service._generate_content_hash(content)
        hash2 = self.service._generate_content_hash(content)
        hash3 = self.service._generate_content_hash("Different content")
        
        # Assert
        assert len(hash1) == 64  # SHA-256 hash length
        assert hash1 == hash2  # Same content should produce same hash
        assert hash1 != hash3  # Different content should produce different hash
    
    def test_split_by_semantic_boundaries(self):
        # Arrange
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        chunk_size = 30  # Small chunk size to force splitting
        
        # Act
        chunks = self.service._split_by_semantic_boundaries(text, chunk_size, 0)
        
        # Assert
        assert len(chunks) >= 2  # Should be split into multiple chunks
        for chunk in chunks:
            assert len(chunk) <= chunk_size + 10  # Allow some flexibility
            assert len(chunk) > 0