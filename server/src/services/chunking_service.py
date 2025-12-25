import re
from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.models.text_chunk import TextChunk
from src.models.clean_text import CleanText
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.config.settings import settings
import hashlib


class ChunkingService(BaseService):
    """
    Service for chunking large documents into smaller segments for embedding
    """
    
    def __init__(self):
        super().__init__("ChunkingService")
    
    def chunk_text(self, clean_text: CleanText) -> Dict[str, Any]:
        """
        Split text into chunks of appropriate size while preserving semantic boundaries
        
        Args:
            clean_text: CleanText model with content to chunk
            
        Returns:
            Dictionary with success status and either list of chunks or error
        """
        try:
            # Split the text while respecting semantic boundaries
            chunks = self._split_by_semantic_boundaries(
                clean_text.clean_content, 
                settings.chunk_size, 
                settings.overlap
            )
            
            # Create TextChunk model instances
            text_chunks = []
            for idx, chunk_content in enumerate(chunks):
                chunk = TextChunk(
                    id=generate_uuid(),
                    content=chunk_content,
                    url=clean_text.original_url,
                    chunk_index=idx,
                    token_count=self._estimate_token_count(chunk_content),
                    hash=self._generate_content_hash(chunk_content),
                    created_at=get_current_timestamp(),
                    metadata={"original_text_id": clean_text.id}
                )
                text_chunks.append(chunk)
            
            return self.handle_success(data=text_chunks, message=f"Text chunked into {len(text_chunks)} chunks")
        
        except Exception as e:
            return self.handle_error(e, "chunk_text")
    
    def _split_by_semantic_boundaries(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Split text by respecting semantic boundaries like paragraphs, sentences, etc.
        
        Args:
            text: Text to split
            chunk_size: Target size for chunks
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        # First, try to split by paragraphs
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                # Add the current chunk to the list
                chunks.append(current_chunk.strip())
                
                # Start a new chunk with overlap if possible
                if overlap > 0 and len(paragraph) > overlap:
                    # Add overlap from the end of the current chunk
                    words = current_chunk.split()
                    overlap_words = words[-(overlap//5):] if len(words) > (overlap//5) else words
                    current_chunk = ' '.join(overlap_words) + ' ' + paragraph
                else:
                    current_chunk = paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += '\n\n' + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # If we still have chunks that are too large, split them by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > chunk_size:
                # Split by sentences
                sentences = re.split(r'[.!?]+', chunk)
                temp_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                        
                    if len(temp_chunk) + len(sentence) > chunk_size and temp_chunk:
                        # Add the current chunk to the list
                        final_chunks.append(temp_chunk.strip())
                        
                        # Start a new chunk with overlap
                        if overlap > 0 and len(sentence) > overlap:
                            words = temp_chunk.split()
                            overlap_words = words[-(overlap//5):] if len(words) > (overlap//5) else words
                            temp_chunk = ' '.join(overlap_words) + ' ' + sentence
                        else:
                            temp_chunk = sentence
                    else:
                        if temp_chunk:
                            temp_chunk += '. ' + sentence
                        else:
                            temp_chunk = sentence
                
                # Add the last temp chunk if it has content
                if temp_chunk.strip():
                    final_chunks.append(temp_chunk.strip())
            else:
                final_chunks.append(chunk)
        
        # Final check: if any chunks are still too large, do a hard split
        result_chunks = []
        for chunk in final_chunks:
            if len(chunk) > chunk_size:
                # Do a hard split at the chunk_size limit
                for i in range(0, len(chunk), chunk_size - overlap):
                    sub_chunk = chunk[i:i + chunk_size]
                    if sub_chunk.strip():
                        result_chunks.append(sub_chunk)
            else:
                result_chunks.append(chunk)
        
        return result_chunks
    
    def _estimate_token_count(self, text: str) -> int:
        """
        Estimate the number of tokens in the text (rough estimation)
        In practice, you might want to use a proper tokenizer like tiktoken
        
        Args:
            text: Text to estimate token count for
            
        Returns:
            Estimated token count
        """
        # A rough estimation: 1 token ~ 4 characters for English text
        # This is a simplified approach; for production, use tiktoken
        return len(text) // 4
    
    def _generate_content_hash(self, content: str) -> str:
        """
        Generate a hash for the content to use for idempotency checks
        
        Args:
            content: Content to hash
            
        Returns:
            SHA-256 hash of the content
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def chunk_with_code_block_preservation(self, clean_text: CleanText) -> Dict[str, Any]:
        """
        Specialized chunking that preserves code blocks and other special formatting
        
        Args:
            clean_text: CleanText model with content to chunk
            
        Returns:
            Dictionary with success status and either list of chunks or error
        """
        try:
            # For now, use the same chunking method
            # In the future, this could have special logic to preserve code blocks
            return self.chunk_text(clean_text)
        except Exception as e:
            return self.handle_error(e, "chunk_with_code_block_preservation")