# API Contract: URL Ingestion & Embedding Pipeline

**Feature**: URL Ingestion & Embedding Pipeline | **Date**: 2025-12-24 | **Branch**: `001-url-ingestion-pipeline`

## Overview

This document defines the API contract for the URL ingestion pipeline service that handles the processing of web content for vector storage and retrieval.

## API Endpoints

### 1. Ingest URLs

**Endpoint**: `POST /api/v1/ingest-urls`

**Description**: Initiates the ingestion process for content from provided URLs

**Request**:
```json
{
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ],
  "options": {
    "force_reprocess": false,
    "chunk_size": 800,
    "overlap": 100
  }
}
```

**Request Parameters**:
- `urls` (array[string], required): Array of URLs to ingest
- `options.force_reprocess` (boolean, optional): Whether to reprocess content even if previously processed (default: false)
- `options.chunk_size` (integer, optional): Target size for text chunks in tokens (default: 800)
- `options.overlap` (integer, optional): Overlap between chunks in tokens (default: 100)

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "in_progress",
  "total_urls": 2,
  "message": "Ingestion job started successfully"
}
```

**Response (Error)**:
```json
{
  "error": "invalid_urls",
  "message": "One or more URLs are invalid or could not be processed"
}
```

**HTTP Status Codes**:
- `202`: Ingestion job accepted and started
- `400`: Invalid request parameters
- `500`: Internal server error during ingestion setup

### 2. Get Ingestion Job Status

**Endpoint**: `GET /api/v1/ingest-urls/{job_id}`

**Description**: Retrieves the current status of an ingestion job

**Path Parameters**:
- `job_id` (string, required): ID of the ingestion job to query

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "embedding",
  "total_urls": 10,
  "processed_urls": 6,
  "successful_chunks": 45,
  "failed_chunks": 2,
  "start_time": "2025-12-24T10:30:00Z",
  "end_time": null,
  "progress_percentage": 60.0
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

### 3. Bulk Ingest from Config

**Endpoint**: `POST /api/v1/bulk-ingest`

**Description**: Initiates ingestion from a configuration file containing multiple URLs and settings

**Request**:
```json
{
  "config": {
    "urls": [
      "https://example.com/article1",
      "https://example.com/article2"
    ],
    "settings": {
      "chunk_size": 600,
      "model": "embed-english-v3.0",
      "metadata": {
        "source_type": "documentation",
        "tags": ["tutorial", "python"]
      }
    }
  }
}
```

**Response (Success)**:
```json
{
  "job_id": "uuid-string",
  "status": "in_progress",
  "total_urls": 2,
  "message": "Bulk ingestion job started successfully"
}
```

**HTTP Status Codes**:
- `202`: Bulk ingestion job accepted and started
- `400`: Invalid configuration
- `500`: Internal server error

### 4. Cancel Ingestion Job

**Endpoint**: `DELETE /api/v1/ingest-urls/{job_id}`

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
- `invalid_urls`: Provided URLs are invalid or could not be processed

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