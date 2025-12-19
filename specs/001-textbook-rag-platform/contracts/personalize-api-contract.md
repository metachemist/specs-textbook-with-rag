# API Contract: Personalize Endpoint

**Feature**: AI-Native Textbook with RAG Platform
**Date**: 2025-12-19
**Contract**: POST /api/personalize

## Overview
This contract defines the API endpoint for personalizing textbook content based on user profile information.

## Endpoint Details
- **Method**: POST
- **Path**: /api/personalize
- **Content-Type**: application/json
- **Authentication**: Required (Bearer token)

## Request

### Headers
- `Authorization: Bearer {token}`
- `Content-Type: application/json`

### Body
```json
{
  "content": "string (the page content to be personalized)",
  "userProfile": {
    "softwareBackground": "string (user's software experience level)",
    "hardwareBackground": "string (user's hardware experience level)"
  },
  "userId": "string (user identifier)"
}
```

### Validation Rules
- `content` is required and must be between 1-10000 characters
- `userProfile` is required with both softwareBackground and hardwareBackground
- `userId` is required and must match the authenticated user

## Response

### Success (200 OK)
```json
{
  "id": "string (unique identifier for the personalized content)",
  "personalizedContent": "string (the personalized markdown content)",
  "userId": "string (user identifier)",
  "originalContentId": "string (identifier of the original content)",
  "timestamp": "string (ISO 8601 timestamp)"
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

#### 403 Forbidden
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
  "content": "# ROS 2 Nodes\nIn ROS 2, nodes are...",
  "userProfile": {
    "softwareBackground": "Python expert with 5+ years experience",
    "hardwareBackground": "Beginner with basic electronics knowledge"
  },
  "userId": "user123"
}
```

## Example Response
```json
{
  "id": "personalized456",
  "personalizedContent": "# ROS 2 Nodes for Python Experts\nAs a Python expert, you can think of ROS 2 nodes as...",
  "userId": "user123",
  "originalContentId": "chapter789",
  "timestamp": "2025-12-19T10:35:00Z"
}
```