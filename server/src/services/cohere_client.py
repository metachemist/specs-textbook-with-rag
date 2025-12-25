import cohere
from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.models.query import Query
from src.models.query_vector import QueryVector
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.config.settings import settings
import time


class CohereClientWrapper(BaseService):
    """
    Wrapper for Cohere API client to handle embedding generation
    """

    def __init__(self):
        super().__init__("CohereClientWrapper")
        self.client = cohere.Client(settings.cohere_api_key)
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # Minimum delay between requests in seconds (adjust as needed)

    def get_embedding(self, text: str) -> Dict[str, Any]:
        """
        Generate embedding for a single text using Cohere API

        Args:
            text: Input text to generate embedding for

        Returns:
            Dictionary with success status and either embedding vector or error
        """
        try:
            # Input validation
            validation_result = self._validate_input(text)
            if not validation_result["success"]:
                return validation_result

            # Rate limiting
            self._enforce_rate_limit()

            # Generate embedding using Cohere API with search_query input type
            response = self.client.embed(
                texts=[text],
                model="embed-english-v3.0",
                input_type="search_query"  # Using search_query as recommended for queries
            )

            # Extract the embedding vector from the response
            embedding_vector = response.embeddings[0]  # Single text, so first element

            # Create Query model instance
            query = Query(text=text)

            # Create QueryVector model instance
            query_vector = QueryVector(
                query_id=query.id,
                vector=embedding_vector,
                model="embed-english-v3.0"
            )

            return self.handle_success(
                data=query_vector,
                message="Embedding generated successfully"
            )

        except Exception as e:
            return self.handle_error(e, "get_embedding")

    def get_embeddings_batch(self, texts: List[str], batch_size: int = 96) -> Dict[str, Any]:
        """
        Generate embeddings for a batch of texts using Cohere API

        Args:
            texts: List of input texts to generate embeddings for
            batch_size: Size of batches to send to Cohere API (max 96)

        Returns:
            Dictionary with success status and either list of embedding vectors or error
        """
        try:
            all_embeddings = []

            # Process in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                # Rate limiting
                self._enforce_rate_limit()

                # Generate embeddings for the batch
                response = self.client.embed(
                    texts=batch,
                    model="embed-english-v3.0",
                    input_type="search_query"  # Using search_query as recommended for queries
                )

                # Extract the embedding vectors from the response
                batch_embeddings = response.embeddings
                all_embeddings.extend(batch_embeddings)

            return self.handle_success(
                data=all_embeddings,
                message=f"Generated embeddings for {len(texts)} texts successfully"
            )

        except Exception as e:
            return self.handle_error(e, "get_embeddings_batch")

    def _validate_input(self, text: str) -> Dict[str, Any]:
        """
        Validate input text for embedding generation

        Args:
            text: Input text to validate

        Returns:
            Dictionary with validation result
        """
        if not text or len(text.strip()) == 0:
            return self.handle_error(ValueError("Text cannot be empty"), "_validate_input")

        if len(text) > 5000:  # Arbitrary limit, adjust as needed
            return self.handle_error(ValueError("Text exceeds maximum length of 5000 characters"), "_validate_input")

        return self.handle_success(message="Input validation passed")

    def _enforce_rate_limit(self):
        """
        Enforce rate limiting by enforcing a minimum delay between requests
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

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