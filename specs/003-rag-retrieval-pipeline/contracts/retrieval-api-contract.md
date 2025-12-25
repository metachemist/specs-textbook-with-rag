# API Contract: RAG Retrieval Service

**Feature**: RAG Retrieval & Validation Pipeline | **Date**: 2025-12-24 | **Branch**: `003-rag-retrieval-pipeline`

## Overview

This document defines the API contract for the RAG retrieval service that handles query embedding and vector search functionality.

## API Endpoints

### 1. Search Knowledge Base

**Endpoint**: `POST /api/v1/search`

**Description**: Performs a semantic search in the knowledge base using the provided query

**Request**:
```json
{
  "query": "What is a node?",
  "top_k": 5,
  "filters": {
    "content_type": "documentation",
    "tags": ["tutorial", "beginner"]
  }
}
```

**Request Parameters**:
- `query` (string, required): The text query to search for
- `top_k` (integer, optional): Number of top results to return (default: 5, max: 10)
- `filters` (object, optional): Filters to apply to the search results

**Response (Success)**:
```json
{
  "query_id": "uuid-string",
  "results": [
    {
      "id": "chunk-uuid",
      "content": "A node in robotics is a computational unit that performs specific functions...",
      "score": 0.87,
      "source_url": "https://example.com/docs/nodes",
      "source_file_path": "/docs/nodes.md",
      "chunk_index": 2,
      "metadata": {
        "title": "Understanding Nodes in Robotics",
        "source_domain": "example.com",
        "content_type": "documentation",
        "tags": ["robotics", "architecture", "components"]
      }
    }
  ],
  "total_results": 1,
  "search_time_ms": 120.5,
  "message": "Search completed successfully"
}
```

**Response (Error)**:
```json
{
  "error": "invalid_query",
  "message": "Query must not be empty"
}
```

**HTTP Status Codes**:
- `200`: Search completed successfully
- `400`: Invalid request parameters
- `500`: Internal server error during search

### 2. Get Search Result Details

**Endpoint**: `GET /api/v1/search/{query_id}`

**Description**: Retrieves detailed information about a specific search result

**Path Parameters**:
- `query_id` (string, required): ID of the search query to retrieve

**Response (Success)**:
```json
{
  "query_id": "uuid-string",
  "query_text": "What is a node?",
  "results": [
    {
      "id": "chunk-uuid",
      "content": "A node in robotics is a computational unit that performs specific functions...",
      "score": 0.87,
      "source_url": "https://example.com/docs/nodes",
      "source_file_path": "/docs/nodes.md",
      "chunk_index": 2,
      "metadata": {
        "title": "Understanding Nodes in Robotics",
        "source_domain": "example.com",
        "content_type": "documentation",
        "tags": ["robotics", "architecture", "components"]
      }
    }
  ],
  "total_results": 1,
  "search_time_ms": 120.5,
  "created_at": "2025-12-24T10:30:00Z"
}
```

**Response (Error)**:
```json
{
  "error": "query_not_found",
  "message": "No search results found with the provided query ID"
}
```

**HTTP Status Codes**:
- `200`: Search result retrieved successfully
- `404`: Query not found
- `500`: Internal server error

## Common Error Responses

The API uses the following standard error response format:

```json
{
  "error": "error_code_string",
  "message": "Human-readable error message",
  "details": {
    // Optional additional error details
  }
}
```

### Common Error Codes

- `invalid_request`: Request parameters are invalid or missing required fields
- `not_found`: Requested resource does not exist
- `unauthorized`: Authentication required but not provided or invalid
- `rate_limit_exceeded`: API rate limit has been exceeded
- `internal_error`: An unexpected error occurred in the service
- `service_unavailable`: External service (Cohere, Qdrant) is temporarily unavailable
- `invalid_query`: Query is empty or otherwise invalid

## Authentication

All endpoints require authentication using API key in the header:

```
Authorization: Bearer YOUR_API_KEY
```

Or:

```
X-API-Key: YOUR_API_KEY
```

## Rate Limiting

- Default rate limit: 100 requests per minute per API key
- Embedding generation may have additional service-specific rate limits
- Responses include rate limit headers as per HTTP standards