# Data Model: RAG Retrieval & Validation Pipeline

**Feature**: RAG Retrieval & Validation Pipeline | **Date**: 2025-12-24 | **Branch**: `003-rag-retrieval-pipeline`

## Overview

This document defines the data models for the RAG retrieval pipeline that accepts text queries, converts them to vector embeddings using Cohere, performs cosine similarity search in Qdrant Cloud, and returns the most relevant text chunks with metadata.

## Core Entities

### Query

**Description**: Represents a text query string submitted for retrieval

**Fields**:
- `id` (string): Unique identifier for the query (UUID)
- `text` (string): The actual text query submitted by the user
- `created_at` (datetime): Timestamp when the query was created
- `processed_at` (datetime, optional): Timestamp when the query was processed

**Validation Rules**:
- `text` must not be empty
- `text` length must be between 1 and 2000 characters
- `id` must be a valid UUID

### QueryVector

**Description**: Represents the vectorized form of a text query

**Fields**:
- `query_id` (string): Reference to the original Query ID
- `vector` (array[float]): The embedding vector (1024 dimensions for Cohere embed-english-v3.0)
- `model` (string): The embedding model used (e.g., "embed-english-v3.0")
- `created_at` (datetime): Timestamp when the embedding was generated

**Validation Rules**:
- `vector` must have exactly 1024 dimensions for Cohere embeddings
- `model` must be a valid Cohere embedding model name
- `query_id` must reference an existing Query

### RetrievedChunk

**Description**: Represents a text chunk returned from the vector search with relevance score

**Fields**:
- `id` (string): Unique identifier for the retrieved chunk (UUID)
- `content` (string): The actual text content of the retrieved chunk
- `score` (float): Relevance score from the vector search (0.0 to 1.0)
- `source_url` (string): URL where the original content is located
- `source_file_path` (string): File path of the original content
- `chunk_index` (integer): Sequential index of the chunk within the original document
- `metadata` (object): Additional metadata for the chunk

**Validation Rules**:
- `content` must not be empty
- `score` must be between 0.0 and 1.0
- `source_url` must be a valid URL format
- `source_file_path` must be a valid file path

### RetrievalResult

**Description**: Represents the complete result set with metadata for each chunk

**Fields**:
- `id` (string): Unique identifier for the retrieval result (UUID)
- `query_id` (string): Reference to the original Query ID
- `chunks` (array[RetrievedChunk]): Array of retrieved text chunks
- `total_chunks_found` (integer): Total number of relevant chunks found
- `search_time_ms` (float): Time taken to perform the search in milliseconds
- `created_at` (datetime): Timestamp when the result was created

**Validation Rules**:
- `chunks` must contain between 1 and 10 items
- `total_chunks_found` must be >= 0
- `search_time_ms` must be >= 0
- `query_id` must reference an existing Query

### SearchMetadata

**Description**: Represents associated information (Source URL, File Path) that provides context for retrieved chunks

**Fields**:
- `source_url` (string): The original URL where the content is located
- `source_file_path` (string): File path of the original content
- `title` (string): Title of the source document or section
- `source_domain` (string): Domain of the original URL
- `chunk_index` (integer): Sequential index of the chunk within the document
- `content_type` (string): Type of content (e.g., "article", "documentation", "blog")
- `created_at` (datetime): Timestamp when the metadata was created
- `tags` (array[string]): Array of tags or categories for the content

**Validation Rules**:
- `source_url` must be a valid URL format
- `source_file_path` must be a valid file path
- `title` must not be empty
- `source_domain` must be a valid domain format
- `tags` must be an array of strings

## Qdrant Collection Schema

### Vector Collection: `web_content_embeddings` (reused from ingestion pipeline)

**Vector Configuration**:
- Vector size: 1024 (for Cohere embed-english-v3.0)
- Distance metric: Cosine

**Payload Fields** (same as ingestion pipeline for consistency):
- `content` (string, indexed): The text content of the chunk
- `url` (string, indexed): The original URL where the content is located
- `title` (string, indexed): Title of the web page or document
- `source_domain` (string, indexed): Domain of the original URL
- `chunk_index` (integer, indexed): Sequential index of the chunk within the document
- `content_type` (string, indexed): Type of content (e.g., "article", "documentation", "blog")
- `created_at` (datetime, indexed): Timestamp when the chunk was created
- `tags` (array[string], indexed): Array of tags or categories for the content

**Indexing Strategy**:
- Index `url`, `title`, `source_domain`, and `content_type` for efficient filtering
- Index `chunk_index` for document reconstruction
- Index `tags` for category-based searches

## Relationships

1. **Query → QueryVector**: One-to-one relationship
   - Each query has exactly one corresponding vector representation
   - The Query.id serves as the foreign key to QueryVector.query_id

2. **Query → RetrievalResult**: One-to-one relationship
   - Each query generates exactly one retrieval result
   - The Query.id serves as the foreign key to RetrievalResult.query_id

3. **RetrievalResult → RetrievedChunk**: One-to-many relationship
   - Each retrieval result contains multiple retrieved chunks
   - The RetrievalResult.id is referenced in RetrievedChunk metadata

4. **RetrievedChunk → SearchMetadata**: One-to-one relationship
   - Each retrieved chunk has associated metadata
   - The RetrievedChunk.id is used to link to the metadata

## State Transitions

### Query Processing States

```
created → embedding → searching → completed
              ↓              ↓
           failed ←----------←
```

- `created` → `embedding`: When the query text is received and ready for embedding
- `embedding` → `searching`: When the query vector is generated and ready for search
- `searching` → `completed`: When the vector search is complete and results are compiled
- Any state → `failed`: When a critical error occurs during processing
- `failed` → `embedding`: When retrying a failed query (if partial success)