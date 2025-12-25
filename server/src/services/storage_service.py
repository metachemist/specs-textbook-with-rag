from qdrant_client.http import models
from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.models.embedding import Embedding
from src.models.metadata import Metadata
from src.utils.helpers import get_current_timestamp
from src.config.qdrant_config import qdrant_config
from src.config.settings import settings


class StorageService(BaseService):
    """
    Service for storing embeddings and metadata in Qdrant Cloud
    """
    
    def __init__(self):
        super().__init__("StorageService")
        self.client = qdrant_config.get_client()
        self.collection_name = settings.qdrant_collection_name
    
    def store_embeddings(self, embeddings: List[Embedding], metadata_list: List[Metadata]) -> Dict[str, Any]:
        """
        Store embeddings with appropriate payload metadata in Qdrant
        
        Args:
            embeddings: List of Embedding models to store
            metadata_list: List of Metadata models with associated information
            
        Returns:
            Dictionary with success status and result or error
        """
        try:
            # Ensure the collection exists
            if not qdrant_config.collection_exists():
                qdrant_config.create_collection()
            
            # Prepare points for insertion
            points = []
            for i, embedding in enumerate(embeddings):
                # Get corresponding metadata (assuming same index)
                metadata = metadata_list[i] if i < len(metadata_list) else None
                
                # Prepare payload with metadata
                payload = {
                    "content": metadata.content_type if metadata else "",
                    "url": metadata.url if metadata else embedding.id,
                    "title": metadata.title if metadata else "",
                    "source_domain": metadata.source_domain if metadata else "",
                    "chunk_index": metadata.chunk_index if metadata else i,
                    "content_type": metadata.content_type if metadata else "unknown",
                    "created_at": str(metadata.created_at if metadata else get_current_timestamp()),
                    "tags": metadata.tags if metadata else []
                }
                
                # Create a point
                point = models.PointStruct(
                    id=embedding.id,
                    vector=embedding.vector,
                    payload=payload
                )
                
                points.append(point)
            
            # Upsert points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            return self.handle_success(
                message=f"Successfully stored {len(embeddings)} embeddings in Qdrant collection '{self.collection_name}'"
            )
        
        except Exception as e:
            return self.handle_error(e, "store_embeddings")
    
    def store_single_embedding(self, embedding: Embedding, metadata: Metadata) -> Dict[str, Any]:
        """
        Store a single embedding with metadata in Qdrant
        
        Args:
            embedding: Embedding model to store
            metadata: Metadata model with associated information
            
        Returns:
            Dictionary with success status and result or error
        """
        try:
            # Ensure the collection exists
            if not qdrant_config.collection_exists():
                qdrant_config.create_collection()
            
            # Prepare payload with metadata
            payload = {
                "content": metadata.content_type,
                "url": metadata.url,
                "title": metadata.title,
                "source_domain": metadata.source_domain,
                "chunk_index": metadata.chunk_index,
                "content_type": metadata.content_type,
                "created_at": str(metadata.created_at),
                "tags": metadata.tags
            }
            
            # Create a point
            point = models.PointStruct(
                id=embedding.id,
                vector=embedding.vector,
                payload=payload
            )
            
            # Upsert point to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            return self.handle_success(
                message=f"Successfully stored embedding in Qdrant collection '{self.collection_name}'"
            )
        
        except Exception as e:
            return self.handle_error(e, "store_single_embedding")
    
    def check_collection_exists(self) -> bool:
        """
        Check if the target collection exists in Qdrant
        
        Returns:
            True if collection exists, False otherwise
        """
        return qdrant_config.collection_exists()
    
    def create_collection_if_not_exists(self) -> Dict[str, Any]:
        """
        Create the collection if it doesn't exist
        
        Returns:
            Dictionary with success status and result or error
        """
        try:
            success = qdrant_config.create_collection()
            if success:
                return self.handle_success(message=f"Collection '{self.collection_name}' is ready")
            else:
                return self.handle_error(Exception(f"Failed to create collection '{self.collection_name}'"), "create_collection_if_not_exists")
        except Exception as e:
            return self.handle_error(e, "create_collection_if_not_exists")
    
    def retrieve_similar(self, query_vector: List[float], limit: int = 10) -> Dict[str, Any]:
        """
        Retrieve similar embeddings from Qdrant
        
        Args:
            query_vector: Vector to search for similarities
            limit: Maximum number of results to return
            
        Returns:
            Dictionary with success status and search results or error
        """
        try:
            # Perform search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )
            
            return self.handle_success(
                data=search_results,
                message=f"Retrieved {len(search_results)} similar embeddings"
            )
        
        except Exception as e:
            return self.handle_error(e, "retrieve_similar")