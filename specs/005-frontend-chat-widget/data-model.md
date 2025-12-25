# Data Model: Frontend Chat Widget Integration

**Feature**: Frontend Chat Widget Integration | **Date**: 2025-12-25 | **Branch**: `005-frontend-chat-widget`

## Overview

This document defines the data models for the Frontend Chat Widget Integration that enables students to interact with the AI assistant directly from any page in the textbook website. The implementation includes chat messages, session state, and API response handling.

## Core Entities

### ChatMessage

**Description**: Represents a single message in the conversation; contains sender type (user/ai), content, timestamp, and status (sent, delivered, error)

**Fields**:
- `id` (string): Unique identifier for the message
- `sender` (string): Type of sender ("user" or "ai")
- `content` (string): The actual content of the message
- `timestamp` (datetime): When the message was created/sent
- `status` (string): Status of the message ("sent", "delivered", "error")
- `error` (string, optional): Error message if status is "error"

**Validation Rules**:
- `sender` must be either "user" or "ai"
- `content` must not be empty
- `timestamp` must be a valid datetime
- `status` must be one of "sent", "delivered", "error"

### ChatSession

**Description**: Represents a single session of the chat widget; contains the list of messages and widget state (open/closed)

**Fields**:
- `id` (string): Unique identifier for the session
- `messages` (array[ChatMessage]): List of messages in the conversation
- `isOpen` (boolean): Whether the chat widget is currently open or closed
- `createdAt` (datetime): When the session was created
- `updatedAt` (datetime): When the session was last updated

**Validation Rules**:
- `messages` must be an array of ChatMessage objects
- `isOpen` must be a boolean value
- `createdAt` must be a valid datetime
- `updatedAt` must be a valid datetime

### APIResponse

**Description**: Represents the response from the backend API; contains the AI-generated response and any metadata

**Fields**:
- `success` (boolean): Whether the API call was successful
- `response` (string): The AI-generated response content
- `sources` (array[string]): List of source files/chapters used by the AI
- `timestamp` (datetime): When the response was generated
- `error` (string, optional): Error message if success is false

**Validation Rules**:
- `success` must be a boolean value
- If `success` is true, `response` must not be empty
- `sources` must be an array of strings
- `timestamp` must be a valid datetime

## State Transitions

### Chat Widget States

```
hidden → opening → visible → interacting → closing → hidden
                ↓                     ↓
              error ←--------------- error
```

- `hidden` → `opening`: When user clicks the floating chat button
- `opening` → `visible`: When the chat window is fully rendered
- `visible` → `interacting`: When user starts typing or sending messages
- `interacting` → `visible`: When user stops typing but keeps window open
- `visible` → `closing`: When user clicks close button or outside the widget
- `interacting` → `error`: When an API call fails during interaction
- `error` → `interacting`: When user retries after an error
- `closing` → `hidden`: When the widget is fully closed

### Message Status Transitions

```
created → sending → sent → delivered
                    ↓
                  error
```

- `created` → `sending`: When user submits a message
- `sending` → `sent`: When the message is successfully sent to the backend
- `sent` → `delivered`: When the message has been acknowledged by the backend
- `sending` → `error`: When there's a failure during the sending process
- `sent` → `error`: When the backend returns an error for the sent message

## Relationships

1. **ChatSession → ChatMessage**: One-to-many relationship
   - Each chat session contains multiple messages
   - The ChatSession.id is used to group related ChatMessage objects

2. **ChatMessage → APIResponse**: One-to-one relationship (for AI messages)
   - Each AI-generated message originates from an API response
   - The ChatMessage.content comes from the APIResponse.response

## API Contract

### Request Format

When sending a message to the backend API:

```json
{
  "message": "The user's message content"
}
```

### Response Format

When receiving a response from the backend API:

```json
{
  "success": true,
  "response": "The AI-generated response",
  "sources": ["source_file_1.md", "source_file_2.md"],
  "timestamp": "2025-12-25T10:30:00Z"
}
```

### Error Response Format

When an error occurs in the backend API:

```json
{
  "success": false,
  "error": "Descriptive error message",
  "timestamp": "2025-12-25T10:30:00Z"
}
```