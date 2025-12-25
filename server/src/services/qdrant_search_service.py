from qdrant_client.http import models
from typing import Dict, Any, List, Optional
from src.services.base_service import BaseService
from src.config.qdrant_config import qdrant_config
from src.models.retrieved_chunk import RetrievedChunk
from src.models.search_metadata import SearchMetadata
from src.models.retrieval_result import RetrievalResult
from src.config.settings import settings
import time


class QdrantSearchService(BaseService):
    """
    Service for performing cosine similarity searches in Qdrant Cloud
    """
    
    def __init__(self):
        super().__init__("QdrantSearchService")
        self.client = qdrant_config.get_client()
        self.collection_name = settings.qdrant_collection_name
    
    def search(self, query_vector: List[float], top_k: int = 5, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform cosine similarity search in Qdrant
        
        Args:
            query_vector: The query vector to search for
            top_k: Number of top results to return (default: 5, max: 10)
            filters: Optional filters to apply to the search results
            
        Returns:
            Dictionary with success status and either search results or error
        """
        try:
            start_time = time.time()
            
            # Prepare filters if provided
            search_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, list):
                        # For list values, create a has_id condition or keyword filter
                        conditions.append(models.FieldCondition(
                            key=key,
                            match=models.MatchAny(any=value)
                        ))
                    else:
                        # For single values, create an exact match condition
                        conditions.append(models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        ))
                
                if conditions:
                    search_filter = models.Filter(must=conditions)
            
            # Perform the search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=top_k,
                with_payload=True,  # Include payload data in results
                with_vectors=False  # We don't need the vectors back
            )
            
            # Process the results into RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                # Extract payload data
                payload = result.payload
                
                # Create SearchMetadata from payload
                metadata = SearchMetadata(
                    source_url=payload.get("url", ""),
                    source_file_path=payload.get("source_file_path", "") if "source_file_path" in payload else payload.get("file_path", ""),
                    title=payload.get("title", ""),
                    source_domain=payload.get("source_domain", ""),
                    chunk_index=payload.get("chunk_index", 0),
                    content_type=payload.get("content_type", "unknown"),
                    tags=payload.get("tags", []),
                    created_at=payload.get("created_at", "")
                )
                
                # Create RetrievedChunk object
                chunk = RetrievedChunk(
                    content=payload.get("content", ""),
                    score=float(result.score),  # Convert to float explicitly
                    source_url=payload.get("url", ""),
                    source_file_path=payload.get("source_file_path", "") if "source_file_path" in payload else payload.get("file_path", ""),
                    chunk_index=payload.get("chunk_index", 0),
                    metadata=metadata.dict()
                )
                
                retrieved_chunks.append(chunk)
            
            # Calculate search time
            search_time_ms = (time.time() - start_time) * 1000
            
            # Create RetrievalResult object
            retrieval_result = RetrievalResult(
                query_id="",  # This would normally come from the original query
                chunks=retrieved_chunks,
                total_chunks_found=len(retrieved_chunks),
                search_time_ms=search_time_ms
            )
            
            return self.handle_success(
                data=retrieval_result,
                message=f"Found {len(retrieved_chunks)} relevant chunks"
            )
            
        except Exception as e:
            return self.handle_error(e, "search")
    
    def search_with_filters(self, query_vector: List[float], top_k: int = 5, 
                           content_type: Optional[str] = None, 
                           source_domain: Optional[str] = None,
                           tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform search with specific filters
        
        Args:
            query_vector: The query vector to search for
            top_k: Number of top results to return
            content_type: Filter by content type
            source_domain: Filter by source domain
            tags: Filter by tags
            
        Returns:
            Dictionary with success status and either search results or error
        """
        try:
            # Build filters dictionary
            filters = {}
            if content_type:
                filters["content_type"] = content_type
            if source_domain:
                filters["source_domain"] = source_domain
            if tags:
                filters["tags"] = tags
            
            # Perform the search with filters
            return self.search(query_vector, top_k, filters)
            
        except Exception as e:
            return self.handle_error(e, "search_with_filters")
    
    def verify_collection_exists(self) -> bool:
        """
        Verify that the target collection exists in Qdrant
        
        Returns:
            True if collection exists, False otherwise
        """
        try:
            self.client.get_collection(self.collection_name)
            return True
        except:
            return False