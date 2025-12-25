# Data Model: RAG Agent with OpenAI Tool Use

**Feature**: RAG Agent with OpenAI Tool Use | **Date**: 2025-12-25 | **Branch**: `004-rag-agent-openai-tool`

## Overview

This document defines the data models for the RAG Agent with OpenAI Tool Use that defines a retrieval tool function, implements agent logic using OpenAI Chat Completions API with tools definitions, configures the AI to act as a "Textbook Assistant" that answers strictly based on retrieved context, implements citation logic to mention source chapters/files, and creates a standalone test script to validate the complete workflow.

## Core Entities

### RetrievalTool

**Description**: Represents the function that the AI can call to retrieve textbook content; has parameters for the search query and returns relevant text chunks with source information

**Fields**:
- `name` (string): The name of the tool ("search_knowledge_base")
- `description` (string): A description of what the tool does
- `parameters` (object): The parameters the tool accepts, defined in JSON Schema format
  - `type` (string): The type of the parameters object ("object")
  - `properties` (object): The properties of the parameters
    - `query` (object): The search query parameter
      - `type` (string): The type of the query parameter ("string")
      - `description` (string): Description of the query parameter
  - `required` (array[string]): List of required parameters (["query"])

**Validation Rules**:
- `name` must be a valid identifier
- `parameters` must follow JSON Schema format
- `query` parameter must be defined in the schema

### AgentRequest

**Description**: Represents a user query submitted to the AI agent; contains the question text and any relevant metadata

**Fields**:
- `id` (string): Unique identifier for the request (UUID)
- `message` (string): The user's query or message to the agent
- `timestamp` (datetime): When the request was created
- `metadata` (object): Additional metadata associated with the request

**Validation Rules**:
- `message` must not be empty
- `message` length must be between 1 and 2000 characters
- `id` must be a valid UUID

### AgentResponse

**Description**: Represents the AI's response to the user; contains the answer text and source citations

**Fields**:
- `id` (string): Unique identifier for the response (UUID)
- `request_id` (string): Reference to the original AgentRequest ID
- `content` (string): The agent's response content
- `citations` (array[Citation]): List of citations used in the response
- `tool_calls` (array[object]): List of tools called during processing
- `timestamp` (datetime): When the response was generated
- `status` (string): Status of the response ("success", "error", "fallback")

**Validation Rules**:
- `content` must not be empty
- `request_id` must reference an existing AgentRequest
- `citations` must be valid Citation objects if present
- `status` must be one of the allowed values

### RetrievedContext

**Description**: Represents the context retrieved by the tool; contains text chunks with source file/chapter information

**Fields**:
- `query` (string): The original query that generated this context
- `chunks` (array[object]): Array of retrieved text chunks
  - `content` (string): The actual text content of the chunk
  - `score` (float): Relevance score of the chunk
  - `source_url` (string): URL where the original content is located
  - `source_file_path` (string): File path of the original content
  - `chunk_index` (integer): Sequential index of the chunk within the original document
- `total_chunks_found` (integer): Total number of chunks retrieved
- `retrieval_time_ms` (float): Time taken to retrieve the context

**Validation Rules**:
- `chunks` must contain at least 1 item
- `total_chunks_found` must be >= 0
- `retrieval_time_ms` must be >= 0
- Each chunk must have valid content and source information

### Citation

**Description**: Represents the source attribution for information in the agent's response; contains chapter/file reference and possibly page numbers or section titles

**Fields**:
- `id` (string): Unique identifier for the citation (UUID)
- `source_file_path` (string): File path of the source document
- `source_url` (string): URL of the source document
- `chapter` (string): Chapter or section title (if applicable)
- `page_number` (integer, optional): Page number (if applicable)
- `text_preview` (string): Preview of the text that was cited
- `confidence_score` (float): Confidence score of the citation's relevance (0.0 to 1.0)

**Validation Rules**:
- `source_file_path` must not be empty
- `text_preview` must not be empty
- `confidence_score` must be between 0.0 and 1.0
- `id` must be a valid UUID

## Relationships

1. **AgentRequest → AgentResponse**: One-to-one relationship
   - Each agent request generates exactly one response
   - The AgentRequest.id serves as the foreign key to AgentResponse.request_id

2. **AgentResponse → Citation**: One-to-many relationship
   - Each agent response can contain multiple citations
   - Citations are linked to the response via the response context

3. **RetrievedContext → Citation**: One-to-many relationship
   - Retrieved context can be used to generate multiple citations
   - Citations are created from the source information in retrieved chunks

## State Transitions

### Agent Processing States

```
received → processing → tool_call_needed → tool_executed → response_generated
     ↓              ↓              ↓              ↓              ↓
   failed ←---------←--------------←--------------←--------------←
```

- `received` → `processing`: When the agent request is received and processing begins
- `processing` → `tool_call_needed`: When the agent determines a tool call is needed
- `tool_call_needed` → `tool_executed`: When the retrieval tool is executed
- `tool_executed` → `response_generated`: When the final response is generated
- `processing` → `response_generated`: When no tool call is needed (direct response)
- Any state → `failed`: When a critical error occurs during processing
- `failed` → `processing`: When retrying a failed request