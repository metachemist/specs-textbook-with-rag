# API Contract: Agent Service

**Feature**: RAG Agent with OpenAI Tool Use | **Date**: 2025-12-25 | **Branch**: `004-rag-agent-openai-tool`

## Overview

This document defines the API contract for the agent service that handles user queries, executes tool calls, and generates responses based on retrieved context.

## API Endpoints

### 1. Generate Agent Response

**Endpoint**: `POST /api/v1/agent/chat`

**Description**: Processes a user message through the AI agent, potentially calling retrieval tools and generating a contextual response

**Request**:
```json
{
  "message": "What is a sensor in robotics?",
  "context": {
    "include_citations": true,
    "max_tokens": 1000
  }
}
```

**Request Parameters**:
- `message` (string, required): The user's query or message to the agent
- `context` (object, optional): Additional context parameters for the request
  - `include_citations` (boolean, optional): Whether to include citations in the response (default: true)
  - `max_tokens` (integer, optional): Maximum number of tokens in the response (default: 1000)

**Response (Success)**:
```json
{
  "response_id": "uuid-string",
  "request_id": "uuid-string",
  "content": "A sensor in robotics is a device that detects and responds to some type of input from the physical environment...",
  "citations": [
    {
      "id": "citation-uuid",
      "source_file_path": "/docs/sensors.md",
      "source_url": "https://example.com/docs/sensors",
      "chapter": "Sensors and Actuators",
      "text_preview": "A sensor in robotics is a device that detects..."
    }
  ],
  "tool_calls": [
    {
      "name": "search_knowledge_base",
      "arguments": {
        "query": "What is a sensor in robotics?"
      },
      "result": {
        "chunks": [
          {
            "content": "A sensor in robotics is a device that detects and responds to some type of input from the physical environment...",
            "source_file_path": "/docs/sensors.md",
            "score": 0.89
          }
        ]
      }
    }
  ],
  "timestamp": "2025-12-25T10:30:00Z",
  "status": "success"
}
```

**Response (Fallback - No Results)**:
```json
{
  "response_id": "uuid-string",
  "request_id": "uuid-string",
  "content": "I don't have information about that topic in the textbook content.",
  "citations": [],
  "tool_calls": [
    {
      "name": "search_knowledge_base",
      "arguments": {
        "query": "What is a sensor in robotics?"
      },
      "result": {
        "chunks": []
      }
    }
  ],
  "timestamp": "2025-12-25T10:30:00Z",
  "status": "fallback"
}
```

**Response (Error)**:
```json
{
  "error": "agent_processing_error",
  "message": "Error processing agent request"
}
```

**HTTP Status Codes**:
- `200`: Agent response generated successfully
- `400`: Invalid request parameters
- `500`: Internal server error during agent processing

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
- `agent_processing_error`: An error occurred during agent processing
- `tool_execution_error`: An error occurred while executing a tool
- `api_connection_error`: External API (OpenAI, Qdrant) connection error
- `rate_limit_exceeded`: API rate limit has been exceeded
- `internal_error`: An unexpected error occurred in the service

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
- Agent processing may have additional service-specific rate limits based on OpenAI usage
- Responses include rate limit headers as per HTTP standards