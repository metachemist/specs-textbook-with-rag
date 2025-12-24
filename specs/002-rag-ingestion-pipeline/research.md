# Research Document: RAG Ingestion Pipeline with Cohere and Qdrant

**Feature**: RAG Ingestion Pipeline | **Date**: 2025-12-24 | **Branch**: `002-rag-ingestion-pipeline`

## Overview

This document captures research findings and technical decisions for implementing the RAG ingestion pipeline that reads markdown content from the `/web` directory, chunks it appropriately for technical textbook content, generates embeddings using the Cohere API, and stores them in Qdrant vector database with metadata.

## Research Findings

### 1. Text Chunking Strategy for Technical Content

**Decision**: Implement a hybrid chunking approach combining semantic boundaries with token limits

**Rationale**: Technical textbook content has complex structures (code examples, mathematical formulas, diagrams) that require careful chunking to maintain semantic meaning. A hybrid approach will:
- Respect document structure (sections, headers)
- Keep code blocks intact
- Maintain logical units of content
- Respect token limits for embedding models

**Implementation approach**:
- Use markdown parsing to identify structural elements
- Apply recursive splitting that respects semantic boundaries
- Set target chunk size to 500-800 tokens to balance context and cost
- Preserve document hierarchy in metadata

**Alternatives considered**:
- Fixed token length chunks: Would break logical concepts
- Header-based chunks only: Might result in very large chunks
- Sentence-based chunks: Would not handle code blocks appropriately

### 2. Cohere Embedding Model Selection

**Decision**: Use `embed-english-v3.0` model with `search_document` input type for textbook content

**Rationale**: 
- Cohere's v3 models offer improved performance and efficiency
- `search_document` type is optimized for document embeddings
- Good performance on technical and educational content
- Cost-effective for large textbook corpus

**Implementation approach**:
- Batch requests to optimize API usage
- Implement retry logic for API failures
- Include proper error handling and rate limiting

**Alternatives considered**:
- `embed-multilingual-v3.0`: Not needed for English-only textbook content
- `embed-english-light-v3.0`: Less accurate than full model
- Previous v2 models: Outdated, less efficient than v3

### 3. Qdrant Vector Database Setup

**Decision**: Use Qdrant Cloud with a dedicated collection for textbook embeddings

**Rationale**:
- Qdrant is the mandated vector database in the constitution
- Cloud version provides scalability and maintenance
- Good performance for semantic search
- Supports metadata filtering needed for textbook content

**Implementation approach**:
- Create collection with appropriate vector dimensions (1024 for Cohere embeddings)
- Define payload schema with metadata fields (URL, title, section, source file)
- Implement upsert logic for idempotency
- Set up proper indexing for metadata fields

**Alternatives considered**:
- Self-hosted Qdrant: More maintenance overhead
- Other vector databases: Would violate constitution tech stack adherence

### 4. Ingestion Pipeline Architecture

**Decision**: Implement as a standalone Python library with clear interfaces

**Rationale**:
- Aligns with the "Library-First Approach" in the constitution
- Enables modularity and reusability
- Supports the separate /server architecture
- Allows for independent testing

**Implementation approach**:
- Create dedicated service classes for each major function
- Implement proper error handling and logging
- Use dependency injection for configuration
- Follow PEP 8 standards

**Alternatives considered**:
- Direct script without modular design: Less maintainable
- Integration into existing services: Would violate library-first principle

### 5. Idempotency Implementation

**Decision**: Use content hash-based deduplication with document-level tracking

**Rationale**:
- Critical requirement to prevent duplicate entries when script runs multiple times
- Content hash ensures that only changed documents are reprocessed
- Document-level tracking allows for incremental updates

**Implementation approach**:
- Calculate hash of document content
- Store document hash and processing status in metadata
- Compare hashes before processing to detect changes
- Implement upsert logic in Qdrant to update existing entries

**Alternatives considered**:
- Timestamp-based: Less reliable as timestamps can change without content changes
- Filename only: Would not detect content changes in same file

## Technical Unknowns Resolved

1. **Chunking strategy**: Resolved to use hybrid approach respecting document structure
2. **Embedding model**: Resolved to use Cohere's embed-english-v3.0
3. **Qdrant configuration**: Resolved to use cloud with appropriate collection settings
4. **Idempotency mechanism**: Resolved to use content hash-based deduplication
5. **Error handling approach**: Resolved to implement comprehensive error handling with retries

## Dependencies to Install

```txt
cohere>=4.0
qdrant-client>=1.9
python-dotenv>=1.0
PyYAML>=6.0
markdown>=3.0
beautifulsoup4>=4.12
pytest>=7.0
```

## Environment Variables Required

```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

## API Rate Limits and Constraints

- Cohere API: Check current rate limits (typically requests/minute and tokens/minute)
- Qdrant Cloud: Verify free tier limitations on storage and requests
- Implement backoff strategies for both services
- Batch operations to optimize API usage