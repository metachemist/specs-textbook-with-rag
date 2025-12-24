# API Contract: RAG Ingestion Pipeline

**Feature**: RAG Ingestion Pipeline | **Date**: 2025-12-24 | **Branch**: `002-rag-ingestion-pipeline`

## Overview

This document defines the API contract for the RAG ingestion pipeline service that handles the processing of textbook content for vector storage and retrieval.

## API Endpoints

### 1. Ingest Content

**Endpoint**: `POST /api/v1/ingest`

**Description**: Initiates the ingestion process for markdown content from the `/web` directory

**Request**:
```json
{
  "source_path": "/web/docs",
  "options": {
    "force_reprocess": false,
    "chunk_size": 800,
    "overlap": 100
  }
}
```

**Request Parameters**:
- `source_path` (string, required): Path to the directory containing markdown files to ingest
- `options.force_reprocess` (boolean, optional): Whether to reprocess documents even if unchanged (default: false)
- `options.chunk_size` (integer, optional): Target size for text chunks in tokens (default: 800)
- `options.overlap` (integer, optional): Overlap between chunks in tokens (default: 100)

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "in_progress",
  "total_documents": 42,
  "message": "Ingestion job started successfully"
}
```

**Response (Error)**:
```json
{
  "error": "invalid_source_path",
  "message": "Source path does not exist or is not readable"
}
```

**HTTP Status Codes**:
- `202`: Ingestion job accepted and started
- `400`: Invalid request parameters
- `500`: Internal server error during ingestion setup

### 2. Get Ingestion Job Status

**Endpoint**: `GET /api/v1/ingest/{job_id}`

**Description**: Retrieves the current status of an ingestion job

**Path Parameters**:
- `job_id` (string, required): ID of the ingestion job to query

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "in_progress",
  "total_documents": 42,
  "processed_documents": 20,
  "successful_chunks": 150,
  "failed_chunks": 2,
  "start_time": "2025-12-24T10:30:00Z",
  "end_time": null,
  "progress_percentage": 47.6
}
```

**Response (Error)**:
```json
{
  "error": "job_not_found",
  "message": "No ingestion job found with the provided ID"
}
```

**HTTP Status Codes**:
- `200`: Job status retrieved successfully
- `404`: Job not found
- `500`: Internal server error

### 3. Verify Indexing

**Endpoint**: `GET /api/v1/verify`

**Description**: Verifies that all expected content has been successfully indexed

**Query Parameters**:
- `source_path` (string, optional): Path to verify; if omitted, checks all indexed content

**Response (Success)**:
```json
{
  "verification_id": "uuid-string",
  "status": "completed",
  "total_expected": 42,
  "total_indexed": 41,
  "missing_documents": [
    {
      "path": "/web/docs/missing-section.md",
      "url": "/docs/missing-section"
    }
  ],
  "timestamp": "2025-12-24T11:00:00Z"
}
```

**Response (Error)**:
```json
{
  "error": "verification_failed",
  "message": "Could not connect to vector database for verification"
}
```

**HTTP Status Codes**:
- `200`: Verification completed successfully
- `500`: Internal server error during verification

### 4. Cancel Ingestion Job

**Endpoint**: `DELETE /api/v1/ingest/{job_id}`

**Description**: Cancels an in-progress ingestion job

**Path Parameters**:
- `job_id` (string, required): ID of the ingestion job to cancel

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "cancelled",
  "message": "Ingestion job cancelled successfully"
}
```

**Response (Error)**:
```json
{
  "error": "job_not_found",
  "message": "No ingestion job found with the provided ID"
}
```

**HTTP Status Codes**:
- `200`: Job cancelled successfully
- `404`: Job not found
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