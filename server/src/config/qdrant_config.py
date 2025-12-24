from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional
from src.config.settings import settings


class QdrantConfig:
    """
    Configuration and initialization for Qdrant client
    """
    
    def __init__(self):
        self.client = None
        self.collection_name = settings.qdrant_collection_name
    
    def get_client(self) -> QdrantClient:
        """
        Get or create the Qdrant client instance
        """
        if self.client is None:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
        return self.client
    
    def create_collection(self) -> bool:
        """
        Create the web_content_embeddings collection with proper schema
        """
        client = self.get_client()
        
        try:
            # Check if collection already exists
            client.get_collection(self.collection_name)
            # If we get here, collection exists
            return True
        except:
            # Collection doesn't exist, create it
            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # For Cohere embeddings
                    distance=models.Distance.COSINE
                )
            )
            
            # Create payload indexes for efficient filtering
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="content",
                field_schema=models.PayloadSchemaType.TEXT
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="url",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="title",
                field_schema=models.PayloadSchemaType.TEXT
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="source_domain",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chunk_index",
                field_schema=models.PayloadSchemaType.INTEGER
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="content_type",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="created_at",
                field_schema=models.PayloadSchemaType.DATETIME
            )
            
            client.create_payload_index(
                collection_name=self.collection_name,
                field_name="tags",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            
            return True
    
    def collection_exists(self) -> bool:
        """
        Check if the collection exists
        """
        try:
            client = self.get_client()
            client.get_collection(self.collection_name)
            return True
        except:
            return False


# Create a singleton instance
qdrant_config = QdrantConfig()