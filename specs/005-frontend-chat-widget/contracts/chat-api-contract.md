# API Contract: Chat Widget Integration

**Feature**: Frontend Chat Widget Integration | **Date**: 2025-12-25 | **Branch**: `005-frontend-chat-widget`

## Overview

This document defines the API contract for the chat widget integration between the Docusaurus frontend and the FastAPI backend. It specifies the endpoints, request/response formats, and error handling for the chat functionality.

## API Endpoints

### 1. Chat Message Endpoint

**Endpoint**: `POST /api/chat`

**Description**: Process a user's message and return an AI-generated response based on textbook content

**Request**:
```json
{
  "message": "What is a sensor in robotics?"
}
```

**Request Parameters**:
- `message` (string, required): The user's message/query to the AI assistant

**Response (Success)**:
```json
{
  "response": "A sensor in robotics is a device that detects and responds to some type of input from the physical environment. The output is obtained in a format that is useful for the robot's controller. Common types of sensors include proximity sensors, light sensors, and temperature sensors...",
  "sources": [
    "docs/sensors.md",
    "docs/perception-systems.md"
  ],
  "timestamp": "2025-12-25T10:30:00Z"
}
```

**Response (Error)**:
```json
{
  "error": "invalid_request",
  "message": "Message field is required and cannot be empty"
}
```

**HTTP Status Codes**:
- `200`: Message processed successfully and response returned
- `400`: Invalid request parameters (empty message, etc.)
- `500`: Internal server error during message processing

### 2. Health Check Endpoint

**Endpoint**: `GET /api/health`

**Description**: Check the health status of the chat API

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-25T10:30:00Z"
}
```

**HTTP Status Codes**:
- `200`: Service is healthy and operational
- `503`: Service is unavailable

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
- `rate_limit_exceeded`: API rate limit has been exceeded
- `service_unavailable`: Backend service (AI model, etc.) is temporarily unavailable
- `internal_error`: An unexpected error occurred in the service
- `message_too_long`: The submitted message exceeds the maximum allowed length

## Authentication

No authentication required for this endpoint in the current scope. (Note: Authentication would be added in future iterations if needed.)

## Rate Limiting

- Default rate limit: 100 requests per user per hour
- Responses include rate limit headers as per HTTP standards

## CORS Policy

- Allowed origins: `http://localhost:3000`, `https://[production-domain].com`
- Allowed methods: `GET`, `POST`
- Allowed headers: `Content-Type`, `Authorization`, `X-Requested-With`
- Credentials allowed: `true`