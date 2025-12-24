from fastapi import APIRouter, HTTPException, Depends, Query, Request
from typing import Dict, Any, Optional
from pydantic import BaseModel, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from rag_service import search_knowledge_base, get_embedding


# Create API router
router = APIRouter(prefix="/api/v1", tags=["retrieval"])

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)


# Request/Response models
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = Query(5, ge=1, le=10, description="Number of top results to return")
    filters: Optional[Dict[str, Any]] = None

    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 1000:  # Max query length
            raise ValueError('Query exceeds maximum length of 1000 characters')
        return v


class SearchResponse(BaseModel):
    query_id: str
    results: list
    total_results: int
    search_time_ms: float
    message: str


def get_api_key(request: Request) -> str:
    """
    Extract API key from Authorization header or X-API-Key header
    """
    auth_header = request.headers.get("Authorization")
    x_api_key = request.headers.get("X-API-Key")

    if auth_header:
        if auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        elif auth_header.startswith("ApiKey "):
            return auth_header[7:]  # Remove "ApiKey " prefix

    if x_api_key:
        return x_api_key

    raise HTTPException(status_code=401, detail="API key is required")


@router.post("/search", response_model=SearchResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def search_endpoint(request: Request, search_request: SearchRequest, api_key: str = Depends(get_api_key)) -> SearchResponse:
    """
    Perform a semantic search in the knowledge base
    """
    try:
        # Perform the search
        result = search_knowledge_base(search_request.query, top_k=search_request.top_k)

        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["message"])

        # Extract data from the result
        retrieval_result = result["data"]

        # Format the response
        formatted_results = []
        for chunk in retrieval_result.chunks:
            formatted_results.append({
                "id": chunk.id,
                "content": chunk.content,
                "score": chunk.score,
                "source_url": chunk.source_url,
                "source_file_path": chunk.source_file_path,
                "chunk_index": chunk.chunk_index,
                "metadata": chunk.metadata
            })

        response = SearchResponse(
            query_id=retrieval_result.query_id,
            results=formatted_results,
            total_results=len(formatted_results),
            search_time_ms=retrieval_result.search_time_ms,
            message=result["message"]
        )

        return response

    except HTTPException:
        raise
    except RateLimitExceeded:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/{query_id}", response_model=SearchResponse)
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
async def get_search_result(request: Request, query_id: str, api_key: str = Depends(get_api_key)) -> SearchResponse:
    """
    Retrieve details of a specific search result
    """
    try:
        # In a real implementation, this would fetch from a database
        # For now, we'll return a placeholder error
        raise HTTPException(status_code=404, detail="Query result not found in this demo implementation")
    except HTTPException:
        raise
    except RateLimitExceeded:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add the rate limit exceeded handler to the app
# This would typically be done in the main app file, but we define it here for completeness
def add_rate_limit_handler(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)