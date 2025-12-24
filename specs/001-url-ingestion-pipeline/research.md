# Research Document: URL Ingestion & Embedding Pipeline

**Feature**: URL Ingestion & Embedding Pipeline | **Date**: 2025-12-24 | **Branch**: `001-url-ingestion-pipeline`

## Overview

This document captures research findings and technical decisions for implementing the URL ingestion pipeline that fetches content from URLs, cleans and chunks the text, generates embeddings using Cohere models, and stores embeddings and metadata in Qdrant Cloud.

## Research Findings

### 1. URL Content Fetching Strategy

**Decision**: Use the `requests` library with custom headers and session management for fetching content

**Rationale**: 
- `requests` is the standard library for HTTP operations in Python
- Provides good error handling and timeout controls
- Supports sessions for connection reuse
- Can handle redirects and cookies appropriately

**Implementation approach**:
- Use custom User-Agent header to avoid blocking by some sites
- Implement timeout and retry mechanisms
- Handle different status codes appropriately
- Support both HTTP and HTTPS protocols

**Alternatives considered**:
- `urllib` from standard library: More verbose, less convenient
- `aiohttp` for async operations: Overkill for this use case
- `selenium` for JavaScript-heavy sites: Would add significant complexity

### 2. Text Cleaning and Processing

**Decision**: Use BeautifulSoup4 with custom cleaning rules to extract meaningful text

**Rationale**:
- BeautifulSoup is the standard for HTML parsing in Python
- Handles malformed HTML gracefully
- Provides precise control over what elements to keep/remove
- Efficient and well-documented

**Implementation approach**:
- Remove script, style, nav, footer elements
- Extract text while preserving paragraph structure
- Handle special characters and encoding properly
- Preserve important semantic elements like headers and lists

**Alternatives considered**:
- Regular expressions: Fragile and not HTML-aware
- `lxml` with XPath: More complex than needed
- `html2text`: May not preserve semantic structure well

### 3. Text Chunking Strategy for Web Content

**Decision**: Implement a hybrid chunking approach combining semantic boundaries with token limits

**Rationale**: 
- Web content has different structure than textbooks (more varied)
- Need to preserve semantic meaning while respecting token limits
- Must handle various content types (articles, documentation, etc.)

**Implementation approach**:
- Use recursive splitting that respects HTML structure
- Set target chunk size to 500-800 tokens
- Keep semantic blocks (paragraphs, lists) together when possible
- Add overlap between chunks to preserve context

**Alternatives considered**:
- Fixed token length chunks: Would break logical concepts
- Header-based chunks only: Might result in very large chunks
- Sentence-based chunks: Would not handle web content structure appropriately

### 4. Cohere Embedding Model Selection

**Decision**: Use `embed-english-v3.0` model with `search_document` input type for web content

**Rationale**:
- Cohere's v3 models offer improved performance and efficiency
- `search_document` type is optimized for document embeddings
- Good performance on diverse web content
- Cost-effective for large web content corpus

**Implementation approach**:
- Batch requests to optimize API usage
- Implement retry logic for API failures
- Include proper error handling and rate limiting

**Alternatives considered**:
- `embed-multilingual-v3.0`: Not needed for English-only content
- `embed-english-light-v3.0`: Less accurate than full model
- Previous v2 models: Outdated, less efficient than v3

### 5. Qdrant Vector Database Setup

**Decision**: Use Qdrant Cloud with a dedicated collection for web content embeddings

**Rationale**:
- Qdrant is the mandated vector database in the constitution
- Cloud version provides scalability and maintenance
- Good performance for semantic search
- Supports metadata filtering needed for web content

**Implementation approach**:
- Create collection with appropriate vector dimensions (1024 for Cohere embeddings)
- Define payload schema with metadata fields (URL, title, timestamp)
- Implement upsert logic for idempotency
- Set up proper indexing for metadata fields

**Alternatives considered**:
- Self-hosted Qdrant: More maintenance overhead
- Other vector databases: Would violate constitution tech stack adherence

### 6. End-to-End Pipeline Architecture

**Decision**: Implement as a standalone Python script with modular service classes

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

## Technical Unknowns Resolved

1. **URL fetching approach**: Resolved to use requests library with custom headers
2. **Text cleaning method**: Resolved to use BeautifulSoup4 with custom rules
3. **Chunking strategy**: Resolved to use hybrid approach respecting document structure
4. **Embedding model**: Resolved to use Cohere's embed-english-v3.0
5. **Qdrant configuration**: Resolved to use cloud with appropriate collection settings
6. **Pipeline architecture**: Resolved to use modular service classes

## Dependencies to Install

```txt
requests>=2.31
beautifulsoup4>=4.12
cohere>=4.0
qdrant-client>=1.9
python-dotenv>=1.0
PyYAML>=6.0
tiktoken>=0.7
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