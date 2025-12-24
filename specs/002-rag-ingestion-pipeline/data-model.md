# Data Model: RAG Ingestion Pipeline

**Feature**: RAG Ingestion Pipeline | **Date**: 2025-12-24 | **Branch**: `002-rag-ingestion-pipeline`

## Overview

This document defines the data models for the RAG ingestion pipeline that reads markdown content from the `/web` directory, chunks it appropriately for technical textbook content, generates embeddings using the Cohere API, and stores them in Qdrant vector database with metadata.

## Core Entities

### TextChunk

**Description**: Represents a segment of processed textbook content with preserved semantic meaning

**Fields**:
- `id` (string): Unique identifier for the chunk (UUID)
- `content` (string): The actual text content of the chunk
- `source_file` (string): Path to the original markdown file
- `url` (string): URL where the content is accessible
- `title` (string): Title of the document or section
- `section` (string): Section header or hierarchy level
- `chunk_index` (integer): Sequential index of the chunk within the document
- `hash` (string): Content hash for idempotency checks
- `created_at` (datetime): Timestamp when the chunk was created
- `updated_at` (datetime): Timestamp when the chunk was last updated
- `metadata` (object): Additional metadata for the chunk

**Validation Rules**:
- `content` must not be empty
- `content` length must be between 10 and 2000 tokens
- `source_file` must be a valid path
- `hash` must be a valid SHA-256 hash string

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

**Description**: Represents associated information (URL, title, section) that provides context for embeddings

**Fields**:
- `url` (string): URL where the content is accessible
- `title` (string): Title of the document or section
- `section` (string): Section header or hierarchy level
- `source_file` (string): Path to the original markdown file
- `chunk_index` (integer): Sequential index of the chunk within the document
- `document_hash` (string): Hash of the entire source document
- `content_type` (string): Type of content (e.g., "textbook", "tutorial", "reference")

**Validation Rules**:
- `url` must be a valid URL format
- `title` must not be empty
- `document_hash` must be a valid SHA-256 hash string

### IngestionJob

**Description**: Represents a single execution of the ingestion process with status tracking

**Fields**:
- `id` (string): Unique identifier for the ingestion job (UUID)
- `status` (string): Current status of the job (e.g., "pending", "in_progress", "completed", "failed")
- `total_documents` (integer): Total number of documents to process
- `processed_documents` (integer): Number of documents processed so far
- `successful_chunks` (integer): Number of chunks successfully embedded
- `failed_chunks` (integer): Number of chunks that failed to process
- `start_time` (datetime): When the job started
- `end_time` (datetime): When the job completed (if finished)
- `error_log` (array[object]): List of errors that occurred during processing

**Validation Rules**:
- `status` must be one of the allowed values
- `total_documents` must be >= 0
- `processed_documents` must be <= `total_documents`
- `successful_chunks` and `failed_chunks` must sum to total processed chunks

## Qdrant Collection Schema

### Vector Collection: `textbook_embeddings`

**Vector Configuration**:
- Vector size: 1024 (for Cohere embed-english-v3.0)
- Distance metric: Cosine

**Payload Fields**:
- `content` (string, indexed): The text content of the chunk
- `url` (string, indexed): URL where the content is accessible
- `title` (string, indexed): Title of the document or section
- `section` (string, indexed): Section header or hierarchy level
- `source_file` (string, indexed): Path to the original markdown file
- `chunk_index` (integer, indexed): Sequential index of the chunk within the document
- `document_hash` (string, indexed): Hash of the entire source document
- `created_at` (datetime, indexed): Timestamp when the chunk was created

**Indexing Strategy**:
- Index `url`, `title`, `section`, and `source_file` for efficient filtering
- Index `document_hash` for idempotency checks
- Index `chunk_index` for document reconstruction

## Relationships

1. **TextChunk → Embedding**: One-to-one relationship
   - Each text chunk has exactly one corresponding embedding
   - The TextChunk.id serves as the foreign key to Embedding.id

2. **TextChunk → Metadata**: One-to-one relationship
   - Each text chunk has associated metadata
   - The TextChunk.id is used to link to the metadata

3. **IngestionJob → TextChunk**: One-to-many relationship
   - Each ingestion job processes multiple text chunks
   - No direct foreign key as chunks are stored in vector database

## State Transitions

### IngestionJob Status Transitions

```
pending → in_progress → completed
           |              ↕
           → failed ←--------
```

- `pending` → `in_progress`: When the ingestion process starts
- `in_progress` → `completed`: When all documents are successfully processed
- `in_progress` → `failed`: When a critical error occurs during processing
- `failed` → `in_progress`: When retrying a failed job
- `failed` → `completed`: When completing a job despite some failures