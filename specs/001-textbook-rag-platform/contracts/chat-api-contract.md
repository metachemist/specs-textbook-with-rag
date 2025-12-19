# API Contract: Chat Endpoint

**Feature**: AI-Native Textbook with RAG Platform
**Date**: 2025-12-19
**Contract**: POST /api/chat

## Overview
This contract defines the API endpoint for handling RAG queries from the textbook interface.

## Endpoint Details
- **Method**: POST
- **Path**: /api/chat
- **Content-Type**: application/json
- **Authentication**: Bearer token (optional for anonymous users)

## Request

### Headers
- `Authorization: Bearer {token}` (optional)
- `Content-Type: application/json`

### Body
```json
{
  "message": "string (the user's question)",
  "currentChapterContext": "string (the current chapter content or identifier)",
  "userId": "string (optional, user identifier if authenticated)"
}
```

### Validation Rules
- `message` is required and must be between 1-1000 characters
- `currentChapterContext` is required
- `userId` is optional but recommended when available

## Response

### Success (200 OK)
```json
{
  "id": "string (unique identifier for the response)",
  "answer": "string (the AI-generated answer based on textbook content)",
  "sources": [
    {
      "title": "string (title of the source)",
      "url": "string (URL to the source content)",
      "excerpt": "string (relevant excerpt from the source)"
    }
  ],
  "timestamp": "string (ISO 8601 timestamp)",
  "queryId": "string (identifier for this query)"
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "error": "string (error message)",
  "code": "string (error code)"
}
```

#### 401 Unauthorized
```json
{
  "error": "string (error message)",
  "code": "string (error code)"
}
```

#### 500 Internal Server Error
```json
{
  "error": "string (error message)",
  "code": "string (error code)"
}
```

## Example Request
```json
{
  "message": "How do ROS 2 nodes communicate with each other?",
  "currentChapterContext": "module1/nodes-topics-services",
  "userId": "user123"
}
```

## Example Response
```json
{
  "id": "resp456",
  "answer": "ROS 2 nodes communicate through topics, services, and actions...",
  "sources": [
    {
      "title": "Nodes and Topics in ROS 2",
      "url": "/docs/module1/nodes-topics-services",
      "excerpt": "In ROS 2, nodes communicate using a publish-subscribe pattern..."
    }
  ],
  "timestamp": "2025-12-19T10:30:00Z",
  "queryId": "query789"
}
```