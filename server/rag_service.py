"""
Main RAG service module for the retrieval pipeline.
Provides functions for embedding text and searching the knowledge base.
"""
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.services.cohere_client import CohereClientWrapper
from src.services.qdrant_search_service import QdrantSearchService
from src.services.result_processor import ResultProcessor
from src.config.qdrant_config import qdrant_config
from src.config.settings import settings


def get_embedding(text: str) -> Dict[str, Any]:
    """
    Generate embedding for a text query using Cohere API
    
    Args:
        text: The text to convert to an embedding
        
    Returns:
        Dictionary containing the embedding vector or error information
    """
    try:
        # Validate environment variables
        if not settings.cohere_api_key or not settings.qdrant_url:
            return {
                "success": False,
                "error": "Missing required environment variables",
                "message": "Both COHERE_API_KEY and QDRANT_URL must be set in environment"
            }
        
        # Create Cohere client wrapper
        cohere_client = CohereClientWrapper()
        
        # Generate embedding
        result = cohere_client.get_embedding(text)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Error in get_embedding: {str(e)}"
        }


def search_knowledge_base(query_text: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search the knowledge base using the provided query text
    
    Args:
        query_text: The text query to search for
        top_k: Number of top results to return (default: 5)
        
    Returns:
        Dictionary containing the search results or error information
    """
    try:
        # Validate environment variables
        if not settings.cohere_api_key or not settings.qdrant_url:
            return {
                "success": False,
                "error": "Missing required environment variables",
                "message": "Both COHERE_API_KEY and QDRANT_URL must be set in environment"
            }
        
        # Step 1: Generate embedding for the query
        embedding_result = get_embedding(query_text)
        
        if not embedding_result["success"]:
            return embedding_result
        
        query_vector = embedding_result["data"].vector
        
        # Step 2: Search in Qdrant
        qdrant_service = QdrantSearchService()
        
        # Perform the search
        search_result = qdrant_service.search(query_vector, top_k=top_k)
        
        if not search_result["success"]:
            return search_result
        
        # Step 3: Process and validate results
        result_processor = ResultProcessor()
        processed_result = result_processor.process_results(
            [{"payload": chunk.metadata, "score": chunk.score} for chunk in search_result["data"].chunks],
            query_id=""  # In a real implementation, we'd have the query ID
        )
        
        if not processed_result["success"]:
            return processed_result
        
        # Return the processed results
        return {
            "success": True,
            "data": processed_result["data"],
            "message": f"Successfully retrieved {len(processed_result['data'].chunks)} results"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Error in search_knowledge_base: {str(e)}"
        }


def initialize_services() -> bool:
    """
    Initialize all required services and verify connections
    
    Returns:
        True if all services initialized successfully, False otherwise
    """
    try:
        # Validate environment variables
        if not settings.cohere_api_key or not settings.qdrant_url:
            print("❌ Environment variables not properly set")
            return False
        
        # Test Cohere connection by generating a simple embedding
        cohere_client = CohereClientWrapper()
        test_embedding_result = cohere_client.get_embedding("test")
        if not test_embedding_result["success"]:
            print(f"❌ Cohere connection test failed: {test_embedding_result['error']}")
            return False
        
        # Test Qdrant connection by checking if collection exists
        if not qdrant_config.collection_exists():
            print("❌ Qdrant collection does not exist")
            return False
        
        print("✅ All services initialized and connections verified")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing services: {str(e)}")
        return False


# If run as main script, run initialization check
if __name__ == "__main__":
    initialize_services()