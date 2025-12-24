# Research Document: RAG Retrieval & Validation Pipeline

**Feature**: RAG Retrieval & Validation Pipeline | **Date**: 2025-12-24 | **Branch**: `003-rag-retrieval-pipeline`

## Overview

This document captures research findings and technical decisions for implementing the RAG retrieval pipeline that accepts text queries, converts them to vector embeddings using Cohere, performs cosine similarity search in Qdrant Cloud, and returns the most relevant text chunks with metadata.

## Research Findings

### 1. Cohere Embedding Model Selection

**Decision**: Use `embed-english-v3.0` model with `search_query` input type for query embedding

**Rationale**:
- Cohere's v3 models offer improved performance and efficiency
- `search_query` type is optimized for search queries (as opposed to `search_document` for stored content)
- Good performance on diverse query types
- Consistency with ingestion pipeline (Spec 1) which uses the same model

**Implementation approach**:
- Call Cohere API with `search_query` input type
- Include proper error handling and rate limiting
- Batch requests when processing multiple queries

**Alternatives considered**:
- `embed-multilingual-v3.0`: Not needed for English-only queries
- `embed-english-light-v3.0`: Less accurate than full model
- Previous v2 models: Outdated, less efficient than v3

### 2. Qdrant Vector Search Configuration

**Decision**: Use cosine similarity with top 3-5 results and appropriate search parameters

**Rationale**:
- Cosine similarity is the standard for semantic search
- 3-5 results provide good balance between relevance and information
- Proper search parameters will optimize for low latency
- Qdrant is the mandated vector database in the constitution

**Implementation approach**:
- Use Qdrant's `search` method with cosine distance
- Limit results to 3-5 with `limit` parameter
- Apply filters if needed for specific metadata
- Optimize for performance with appropriate parameters

**Alternatives considered**:
- Euclidean distance: Less appropriate for high-dimensional embeddings
- Different result counts: Would not match requirements

### 3. RAG Service Architecture

**Decision**: Implement as a standalone Python module with clear interfaces

**Rationale**:
- Aligns with the "Library-First Approach" in the constitution
- Enables modularity and reusability
- Supports the separate /server architecture
- Allows for independent testing

**Implementation approach**:
- Create `rag_service.py` with main functions
- Implement `get_embedding(text)` to wrap Cohere API call
- Implement `search_knowledge_base(query_text)` to orchestrate the process
- Use dependency injection for configuration
- Follow PEP 8 standards

**Alternatives considered**:
- Direct integration without modular design: Less maintainable
- Integration into existing services: Would violate library-first principle

### 4. Configuration Management

**Decision**: Reuse existing environment variables (`COHERE_API_KEY`, `QDRANT_URL`) as mandated

**Rationale**:
- Consistency with the project's configuration approach
- Security: Credentials are already managed properly
- Requirement explicitly stated in feature specification

**Implementation approach**:
- Load environment variables using python-dotenv
- Validate that required variables are present
- Provide clear error messages if variables are missing

**Alternatives considered**:
- New environment variables: Would violate constraint to reuse existing ones
- Configuration files: Would add unnecessary complexity

### 5. Validation Script Approach

**Decision**: Create standalone test script that performs sanity check queries

**Rationale**:
- Enables verification of the retrieval pipeline independently
- Allows for quick validation of search accuracy
- Meets the requirement for standalone testing

**Implementation approach**:
- Create `test_retrieval.py` script
- Implement query like "What is a node?" as example
- Print raw search results (score + payload) to console
- Include proper error handling

**Alternatives considered**:
- Integration testing only: Would not meet standalone testing requirement

## Technical Unknowns Resolved

1. **Embedding model**: Resolved to use Cohere's embed-english-v3.0 with search_query input type
2. **Search algorithm**: Resolved to use cosine similarity with 3-5 results
3. **Service architecture**: Resolved to implement as standalone module
4. **Configuration approach**: Resolved to reuse existing environment variables
5. **Validation method**: Resolved to create standalone test script

## Dependencies to Install

```txt
cohere>=4.0
qdrant-client>=1.9
python-dotenv>=1.0
PyYAML>=6.0
pytest>=7.0
```

## Environment Variables Required

```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key (if required)
```

## API Rate Limits and Constraints

- Cohere API: Check current rate limits (typically requests/minute and tokens/minute)
- Qdrant Cloud: Verify free tier limitations on search requests
- Implement backoff strategies for both services
- Batch operations where possible to optimize API usage