import cohere
from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.models.embedding import Embedding
from src.models.text_chunk import TextChunk
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.config.settings import settings
import time


class EmbeddingService(BaseService):
    """
    Service for generating embeddings using Cohere models
    """
    
    def __init__(self):
        super().__init__("EmbeddingService")
        self.client = cohere.Client(settings.cohere_api_key)
    
    def generate_embeddings(self, text_chunks: List[TextChunk]) -> Dict[str, Any]:
        """
        Generate embeddings for a list of text chunks
        
        Args:
            text_chunks: List of TextChunk models to generate embeddings for
            
        Returns:
            Dictionary with success status and either list of embeddings or error
        """
        try:
            # Extract text content from chunks
            texts = [chunk.content for chunk in text_chunks]
            
            # Generate embeddings using Cohere API
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",  # Using the specified model
                input_type="search_document"  # Using search_document for web content
            )
            
            # Create Embedding model instances
            embeddings = []
            for i, embedding_vector in enumerate(response.embeddings):
                embedding = Embedding(
                    id=text_chunks[i].id,  # Use the chunk's ID as the embedding ID
                    vector=embedding_vector,
                    model="embed-english-v3.0",
                    created_at=get_current_timestamp()
                )
                embeddings.append(embedding)
            
            return self.handle_success(data=embeddings, message=f"Generated embeddings for {len(text_chunks)} chunks")
        
        except Exception as e:
            return self.handle_error(e, "generate_embeddings")
    
    def generate_embeddings_with_retry(self, text_chunks: List[TextChunk], max_retries: int = 3) -> Dict[str, Any]:
        """
        Generate embeddings with retry mechanism for transient failures
        
        Args:
            text_chunks: List of TextChunk models to generate embeddings for
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary with success status and either list of embeddings or error
        """
        last_error = None
        
        for attempt in range(max_retries + 1):
            result = self.generate_embeddings(text_chunks)
            
            # If successful, return immediately
            if result["success"]:
                return result
            
            # If it's the last attempt, break and return the error
            if attempt == max_retries:
                break
            
            # Log the retry attempt and wait before retrying
            self.logger.warning(f"Attempt {attempt + 1} failed for embedding generation, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
            last_error = result["error"]
        
        # If we exhausted all retries, return the last error
        return self.handle_error(
            Exception(f"All {max_retries} retry attempts failed for embedding generation. Last error: {last_error}"),
            "generate_embeddings_with_retry"
        )
    
    def batch_generate_embeddings(self, text_chunks: List[TextChunk], batch_size: int = 96) -> Dict[str, Any]:
        """
        Generate embeddings in batches to optimize API usage and handle rate limits
        
        Args:
            text_chunks: List of TextChunk models to generate embeddings for
            batch_size: Number of chunks to process in each batch (Cohere's limit is 96)
            
        Returns:
            Dictionary with success status and either list of all embeddings or error
        """
        try:
            all_embeddings = []
            
            # Process in batches
            for i in range(0, len(text_chunks), batch_size):
                batch = text_chunks[i:i + batch_size]
                
                # Generate embeddings for the batch
                batch_result = self.generate_embeddings_with_retry(batch)
                
                if not batch_result["success"]:
                    return batch_result
                
                all_embeddings.extend(batch_result["data"])
            
            return self.handle_success(data=all_embeddings, message=f"Generated embeddings for {len(text_chunks)} chunks in batches")
        
        except Exception as e:
            return self.handle_error(e, "batch_generate_embeddings")
    
    def validate_embedding_model(self, model_name: str) -> bool:
        """
        Validate if the embedding model is supported
        
        Args:
            model_name: Name of the embedding model
            
        Returns:
            True if the model is valid, False otherwise
        """
        valid_models = [
            "embed-english-v3.0",
            "embed-multilingual-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-light-v3.0"
        ]
        return model_name in valid_models