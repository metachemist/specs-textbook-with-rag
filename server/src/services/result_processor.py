from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.models.retrieved_chunk import RetrievedChunk
from src.models.search_metadata import SearchMetadata
from src.models.retrieval_result import RetrievalResult
from src.utils.validators import is_valid_url
from src.utils.helpers import get_current_timestamp
import time


class ResultProcessor(BaseService):
    """
    Service for processing retrieval results and validating metadata
    """
    
    def __init__(self):
        super().__init__("ResultProcessor")
    
    def process_results(self, search_results: List[Dict[str, Any]], query_id: str = "") -> Dict[str, Any]:
        """
        Process raw search results into validated RetrievalResult objects
        
        Args:
            search_results: Raw search results from Qdrant
            query_id: ID of the original query
            
        Returns:
            Dictionary with success status and either processed results or error
        """
        try:
            # Process each result into a RetrievedChunk object
            processed_chunks = []
            for result in search_results:
                # Extract payload data
                payload = result.get("payload", {})
                
                # Extract score
                score = result.get("score", 0.0)
                
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
                
                # Validate the metadata
                validation_result = self.validate_metadata(metadata)
                if not validation_result["success"]:
                    self.logger.warning(f"Metadata validation failed for chunk: {validation_result['message']}")
                
                # Create RetrievedChunk object
                chunk = RetrievedChunk(
                    content=payload.get("content", ""),
                    score=float(score),  # Convert to float explicitly
                    source_url=payload.get("url", ""),
                    source_file_path=payload.get("source_file_path", "") if "source_file_path" in payload else payload.get("file_path", ""),
                    chunk_index=payload.get("chunk_index", 0),
                    metadata=metadata.dict()
                )
                
                processed_chunks.append(chunk)
            
            # Create RetrievalResult object
            retrieval_result = RetrievalResult(
                query_id=query_id,
                chunks=processed_chunks,
                total_chunks_found=len(processed_chunks),
                search_time_ms=result.get("search_time_ms", 0.0)
            )
            
            return self.handle_success(
                data=retrieval_result,
                message=f"Processed {len(processed_chunks)} retrieved chunks with validated metadata"
            )
            
        except Exception as e:
            return self.handle_error(e, "process_results")
    
    def validate_metadata(self, metadata: SearchMetadata) -> Dict[str, Any]:
        """
        Validate metadata fields
        
        Args:
            metadata: SearchMetadata object to validate
            
        Returns:
            Dictionary with validation result
        """
        try:
            # Validate source URL
            if not is_valid_url(metadata.source_url):
                return self.handle_error(
                    ValueError(f"Invalid source URL: {metadata.source_url}"),
                    "validate_metadata"
                )
            
            # Validate source file path
            if not metadata.source_file_path or len(metadata.source_file_path.strip()) == 0:
                return self.handle_error(
                    ValueError("Source file path is required"),
                    "validate_metadata"
                )
            
            # Validate title
            if not metadata.title or len(metadata.title.strip()) == 0:
                return self.handle_error(
                    ValueError("Title is required"),
                    "validate_metadata"
                )
            
            # Validate source domain
            if not metadata.source_domain or len(metadata.source_domain.strip()) == 0:
                return self.handle_error(
                    ValueError("Source domain is required"),
                    "validate_metadata"
                )
            
            # Validate tags if present
            if metadata.tags:
                for tag in metadata.tags:
                    if not isinstance(tag, str) or len(tag.strip()) == 0:
                        return self.handle_error(
                            ValueError(f"All tags must be non-empty strings, got: {tag}"),
                            "validate_metadata"
                        )
            
            return self.handle_success(message="Metadata validation passed")
            
        except Exception as e:
            return self.handle_error(e, "validate_metadata")
    
    def calculate_relevance_scores(self, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        """
        Calculate or adjust relevance scores for retrieved chunks
        
        Args:
            chunks: List of RetrievedChunk objects
            
        Returns:
            List of RetrievedChunk objects with adjusted relevance scores
        """
        # For now, just return the chunks as-is
        # In a more sophisticated implementation, we might adjust scores
        # based on additional factors like recency, source authority, etc.
        return chunks
    
    def validate_retrieval_result(self, result: RetrievalResult) -> Dict[str, Any]:
        """
        Validate a complete retrieval result
        
        Args:
            result: RetrievalResult object to validate
            
        Returns:
            Dictionary with validation result
        """
        try:
            # Validate number of chunks
            if len(result.chunks) < 1 or len(result.chunks) > 10:
                return self.handle_error(
                    ValueError(f"Result must contain between 1 and 10 chunks, got {len(result.chunks)}"),
                    "validate_retrieval_result"
                )
            
            # Validate total chunks found
            if result.total_chunks_found < 0:
                return self.handle_error(
                    ValueError("Total chunks found must be >= 0"),
                    "validate_retrieval_result"
                )
            
            # Validate search time
            if result.search_time_ms < 0:
                return self.handle_error(
                    ValueError("Search time must be >= 0"),
                    "validate_retrieval_result"
                )
            
            # Validate each chunk
            for chunk in result.chunks:
                validation_result = self.validate_metadata(SearchMetadata(**chunk.metadata))
                if not validation_result["success"]:
                    return validation_result
            
            return self.handle_success(message="Retrieval result validation passed")
            
        except Exception as e:
            return self.handle_error(e, "validate_retrieval_result")