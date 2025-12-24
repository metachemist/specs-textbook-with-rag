# Data Model: URL Ingestion & Embedding Pipeline

**Feature**: URL Ingestion & Embedding Pipeline | **Date**: 2025-12-24 | **Branch**: `001-url-ingestion-pipeline`

## Overview

This document defines the data models for the URL ingestion pipeline that fetches content from URLs, cleans and chunks the text, generates embeddings using Cohere models, and stores embeddings and metadata in Qdrant Cloud.

## Core Entities

### URLContent

**Description**: Represents the raw content fetched from a URL

**Fields**:
- `id` (string): Unique identifier for the URL content (UUID)
- `url` (string): The original URL that was fetched
- `raw_content` (string): The raw HTML/content fetched from the URL
- `status_code` (integer): HTTP status code from the fetch operation
- `content_type` (string): MIME type of the fetched content
- `fetched_at` (datetime): Timestamp when the content was fetched
- `encoding` (string): Character encoding of the content
- `error_message` (string, optional): Error message if the fetch failed

**Validation Rules**:
- `url` must be a valid URL format
- `raw_content` must not be empty when status_code indicates success
- `status_code` must be a valid HTTP status code
- `fetched_at` must be a valid timestamp

### CleanText

**Description**: Represents the processed text after cleaning and normalization

**Fields**:
- `id` (string): Reference to the URLContent ID
- `clean_content` (string): The cleaned text content
- `original_url` (string): The original URL (denormalized for performance)
- `word_count` (integer): Number of words in the clean content
- `character_count` (integer): Number of characters in the clean content
- `cleaned_at` (datetime): Timestamp when the content was cleaned
- `processing_notes` (string, optional): Notes about the cleaning process

**Validation Rules**:
- `clean_content` must not be empty
- `word_count` and `character_count` must be non-negative
- `original_url` must match the URL in the referenced URLContent

### TextChunk

**Description**: Represents a segment of processed content with preserved semantic meaning

**Fields**:
- `id` (string): Unique identifier for the chunk (UUID)
- `content` (string): The actual text content of the chunk
- `url` (string): The original URL this chunk came from
- `chunk_index` (integer): Sequential index of the chunk within the document
- `token_count` (integer): Number of tokens in the chunk
- `hash` (string): Content hash for idempotency checks
- `created_at` (datetime): Timestamp when the chunk was created
- `metadata` (object): Additional metadata for the chunk

**Validation Rules**:
- `content` must not be empty
- `content` length must be between 10 and 2000 tokens
- `url` must be a valid URL format
- `hash` must be a valid SHA-256 hash string
- `token_count` must be positive

### Embedding

**Description**: Represents a vectorized representation of a text chunk

**Fields**:
- `id` (string): Reference to the TextChunk ID
- `vector` (array[float]): The embedding vector (1024 dimensions for Cohere)
- `model` (string): The embedding model used (e.g., "embed-english-v3.0")
- `created_at` (datetime): Timestamp when the embedding was generated

**Validation Rules**:
- `vector` must have exactly 1024 dimensions for Cohere embeddings
- `model` must be a valid Cohere embedding model name
- `id` must reference an existing TextChunk

### Metadata

**Description**: Represents associated information (URL, title, timestamp) that provides context for embeddings

**Fields**:
- `url` (string): The original URL where the content is located
- `title` (string): Title of the web page or document
- `source_domain` (string): Domain of the original URL
- `chunk_index` (integer): Sequential index of the chunk within the document
- `content_type` (string): Type of content (e.g., "article", "documentation", "blog")
- `created_at` (datetime): Timestamp when the metadata was created
- `tags` (array[string]): Array of tags or categories for the content

**Validation Rules**:
- `url` must be a valid URL format
- `title` must not be empty
- `source_domain` must be a valid domain format
- `tags` must be an array of strings

### IngestionJob

**Description**: Represents a single execution of the ingestion process with status tracking

**Fields**:
- `id` (string): Unique identifier for the ingestion job (UUID)
- `status` (string): Current status of the job (e.g., "pending", "fetching", "cleaning", "chunking", "embedding", "storing", "completed", "failed")
- `urls_to_process` (array[string]): List of URLs to process in this job
- `total_urls` (integer): Total number of URLs to process
- `processed_urls` (integer): Number of URLs processed so far
- `successful_chunks` (integer): Number of chunks successfully embedded
- `failed_chunks` (integer): Number of chunks that failed to process
- `start_time` (datetime): When the job started
- `end_time` (datetime): When the job completed (if finished)
- `error_log` (array[object]): List of errors that occurred during processing

**Validation Rules**:
- `status` must be one of the allowed values
- `total_urls` must be >= 0
- `processed_urls` must be <= `total_urls`
- `successful_chunks` and `failed_chunks` must sum to total processed chunks

## Qdrant Collection Schema

### Vector Collection: `web_content_embeddings`

**Vector Configuration**:
- Vector size: 1024 (for Cohere embed-english-v3.0)
- Distance metric: Cosine

**Payload Fields**:
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

1. **URLContent → CleanText**: One-to-one relationship
   - Each URL content has exactly one cleaned version
   - The URLContent.id serves as the foreign key to CleanText.id

2. **CleanText → TextChunk**: One-to-many relationship
   - Each cleaned text can be split into multiple chunks
   - The CleanText.id is referenced in TextChunk.metadata

3. **TextChunk → Embedding**: One-to-one relationship
   - Each text chunk has exactly one corresponding embedding
   - The TextChunk.id serves as the foreign key to Embedding.id

4. **TextChunk → Metadata**: One-to-one relationship
   - Each text chunk has associated metadata
   - The TextChunk.id is used to link to the metadata

5. **IngestionJob → URLContent**: One-to-many relationship
   - Each ingestion job processes multiple URL contents
   - The IngestionJob.id is tracked in URLContent for job association

## State Transitions

### IngestionJob Status Transitions

```
pending → fetching → cleaning → chunking → embedding → storing → completed
                    ↓          ↓          ↓           ↓             ↓
                   failed ←----←----------←-----------←-------------←
```

- `pending` → `fetching`: When the job starts processing URLs
- `fetching` → `cleaning`: When content fetching is complete
- `cleaning` → `chunking`: When text cleaning is complete
- `chunking` → `embedding`: When chunking is complete
- `embedding` → `storing`: When embeddings are generated
- `storing` → `completed`: When all embeddings are stored in Qdrant
- Any state → `failed`: When a critical error occurs during processing
- `failed` → `fetching`: When retrying a failed job (if partial success)