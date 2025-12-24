# Implementation Tasks: URL Ingestion & Embedding Pipeline

**Feature**: URL Ingestion & Embedding Pipeline | **Date**: 2025-12-24 | **Branch**: `001-url-ingestion-pipeline`

## Overview

This document outlines the implementation tasks for the URL ingestion pipeline that fetches content from URLs, cleans and chunks the text, generates embeddings using Cohere models, and stores embeddings and metadata in Qdrant Cloud.

**Implementation Strategy**: Build the feature incrementally, starting with foundational components, then implementing each user story in priority order. Each user story should be independently testable and deliver value on its own.

## Dependencies

- **US1 (P1) URL Content Fetching** → **US2 (P1) Text Cleaning** → **US3 (P1) Text Chunking** → **US4 (P1) Embedding Generation** → **US5 (P1) Vector Storage in Qdrant**
- **US6 (P2) End-to-End Pipeline Execution** depends on all other user stories

## Parallel Execution Examples

- **US2 (Text Cleaning)** and **US3 (Text Chunking)** can be developed in parallel once **US1 (URL Fetching)** is complete
- **US4 (Embedding Generation)** and **US5 (Vector Storage)** can be developed in parallel once **US3 (Text Chunking)** is complete

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies

- [ ] T001 Create project structure in server/ per implementation plan
- [ ] T002 Create requirements.txt with dependencies: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv, PyYAML, tiktoken, pytest
- [ ] T003 Create .env.example with environment variable placeholders
- [ ] T004 Set up basic configuration in server/src/config/settings.py
- [ ] T005 Create logging utility in server/src/utils/logger.py
- [ ] T006 Create utility functions in server/src/utils/helpers.py
- [ ] T007 Create URL validator in server/src/utils/validators.py

## Phase 2: Foundational Components

**Goal**: Create foundational components that will be used across multiple user stories

- [ ] T008 [P] Create URLContent model in server/src/models/url_content.py
- [ ] T009 [P] Create CleanText model in server/src/models/clean_text.py
- [ ] T010 [P] Create TextChunk model in server/src/models/text_chunk.py
- [ ] T011 [P] Create Embedding model in server/src/models/embedding.py
- [ ] T012 [P] Create Metadata model in server/src/models/metadata.py
- [ ] T013 [P] Create IngestionJob model in server/src/models/ingestion_job.py
- [ ] T014 Create Qdrant client configuration and initialization in server/src/config/qdrant_config.py
- [ ] T015 [P] Create Qdrant collection schema for web_content_embeddings per data model
- [ ] T016 [P] Create base service class in server/src/services/base_service.py

## Phase 3: User Story 1 - URL Content Fetching (Priority: P1)

**Goal**: Implement the ability to fetch content from URLs

**Independent Test Criteria**: Can run the ingestion script with a URL and verify that content is successfully retrieved from that URL.

**Acceptance Scenarios**:
1. Given I have a valid URL with web content, When I run the ingestion script with that URL, Then the content is successfully fetched and processed
2. Given I have an invalid or inaccessible URL, When I run the ingestion script, Then appropriate error handling occurs without crashing the system

- [ ] T017 [US1] Create URL fetch service in server/src/services/url_fetch_service.py
- [ ] T018 [P] [US1] Implement HTTP GET request with requests library and custom headers
- [ ] T019 [P] [US1] Implement timeout and retry mechanisms for URL fetching
- [ ] T020 [P] [US1] Handle different HTTP status codes appropriately
- [ ] T021 [P] [US1] Implement URL validation before fetching
- [ ] T022 [P] [US1] Handle redirects and cookies appropriately
- [ ] T023 [P] [US1] Implement error handling for network issues
- [ ] T024 [P] [US1] Store fetched content in URLContent model with metadata
- [ ] T025 [US1] Write unit tests for URL fetch service in server/tests/unit/test_url_fetch_service.py

## Phase 4: User Story 2 - Text Cleaning and Processing (Priority: P1)

**Goal**: Implement the ability to clean and process raw HTML content into clean text

**Independent Test Criteria**: Can process raw HTML content and verify that it's cleaned of markup while preserving meaningful text.

**Acceptance Scenarios**:
1. Given raw HTML content from a webpage, When the text cleaning process runs, Then HTML tags and scripts are removed while preserving meaningful text
2. Given content with special characters or encoding issues, When the cleaning process runs, Then text is normalized to UTF-8 without losing meaning

- [ ] T026 [US2] Create text cleaning service in server/src/services/text_cleaning_service.py
- [ ] T027 [P] [US2] Implement HTML parsing with BeautifulSoup4
- [ ] T028 [P] [US2] Remove script, style, nav, footer elements from HTML
- [ ] T029 [P] [US2] Extract text while preserving paragraph structure
- [ ] T030 [P] [US2] Handle special characters and encoding properly
- [ ] T031 [P] [US2] Preserve important semantic elements like headers and lists
- [ ] T032 [P] [US2] Create CleanText model instance from cleaned content
- [ ] T033 [P] [US2] Add processing notes to CleanText model
- [ ] T034 [US2] Write unit tests for text cleaning service in server/tests/unit/test_text_cleaning_service.py

## Phase 5: User Story 3 - Text Chunking (Priority: P1)

**Goal**: Implement the ability to properly chunk large documents for embedding

**Independent Test Criteria**: Can process a large text document and verify it's split into appropriately sized chunks that preserve context.

**Acceptance Scenarios**:
1. Given a large text document, When the chunking algorithm runs, Then the document is split into chunks of appropriate size while preserving semantic boundaries
2. Given text that contains code blocks or special formatting, When the chunking algorithm runs, Then these elements are preserved intact within chunks

- [ ] T035 [US3] Create chunking service in server/src/services/chunking_service.py
- [ ] T036 [P] [US3] Implement recursive splitting that respects HTML structure
- [ ] T037 [P] [US3] Set target chunk size to 500-800 tokens
- [ ] T038 [P] [US3] Keep semantic blocks (paragraphs, lists) together when possible
- [ ] T039 [P] [US3] Add overlap between chunks to preserve context
- [ ] T040 [P] [US3] Calculate token counts for each chunk
- [ ] T041 [P] [US3] Generate content hash for idempotency checks
- [ ] T042 [P] [US3] Create TextChunk model instances
- [ ] T043 [US3] Write unit tests for chunking service in server/tests/unit/test_chunking_service.py

## Phase 6: User Story 4 - Embedding Generation (Priority: P1)

**Goal**: Implement the ability to generate embeddings using Cohere models

**Independent Test Criteria**: Can generate embeddings for text chunks and verify they are properly created and formatted.

**Acceptance Scenarios**:
1. Given clean text chunks, When the embedding generation runs, Then high-quality vector embeddings are produced using Cohere models
2. Given Cohere API credentials, When embedding generation runs, Then embeddings are generated without authentication errors

- [ ] T044 [US4] Create embedding service in server/src/services/embedding_service.py
- [ ] T045 [P] [US4] Implement Cohere API client initialization with credentials
- [ ] T046 [P] [US4] Implement embedding generation using embed-english-v3.0 model
- [ ] T047 [P] [US4] Set input type to search_document for web content
- [ ] T048 [P] [US4] Batch requests to optimize API usage
- [ ] T049 [P] [US4] Implement retry logic for API failures
- [ ] T050 [P] [US4] Handle rate limiting with backoff strategies
- [ ] T051 [P] [US4] Create Embedding model instances with vector data
- [ ] T052 [US4] Write unit tests for embedding service in server/tests/unit/test_embedding_service.py

## Phase 7: User Story 5 - Vector Storage in Qdrant (Priority: P1)

**Goal**: Implement the ability to store embeddings and metadata in Qdrant Cloud

**Independent Test Criteria**: Can store embeddings in Qdrant and verify they are properly indexed and searchable.

**Acceptance Scenarios**:
1. Given generated embeddings with metadata, When the storage process runs, Then they are properly indexed in Qdrant Cloud
2. Given stored embeddings, When a retrieval query is made, Then relevant content is returned with proper metadata

- [ ] T053 [US5] Create storage service in server/src/services/storage_service.py
- [ ] T054 [P] [US5] Implement Qdrant client connection with credentials
- [ ] T055 [P] [US5] Create web_content_embeddings collection with proper schema
- [ ] T056 [P] [US5] Implement upsert logic for idempotency
- [ ] T057 [P] [US5] Store embeddings with appropriate payload metadata
- [ ] T058 [P] [US5] Set up proper indexing for metadata fields
- [ ] T059 [P] [US5] Implement error handling for storage operations
- [ ] T060 [US5] Write unit tests for storage service in server/tests/unit/test_storage_service.py

## Phase 8: User Story 6 - End-to-End Pipeline Execution (Priority: P2)

**Goal**: Implement a single function to run the full ingestion pipeline

**Independent Test Criteria**: Can execute the main function and verify that all steps of the pipeline complete successfully.

**Acceptance Scenarios**:
1. Given a list of URLs, When the main() function runs, Then all steps of the pipeline execute successfully from fetching to storage
2. Given the main() function, When it's executed, Then appropriate logging and error handling occur throughout the process

- [ ] T061 [US6] Create ingestion pipeline orchestrator in server/src/services/ingestion_pipeline.py
- [ ] T062 [P] [US6] Implement pipeline workflow: fetch → clean → chunk → embed → store
- [ ] T063 [P] [US6] Track progress through IngestionJob model
- [ ] T064 [P] [US6] Implement error handling and recovery mechanisms
- [ ] T065 [P] [US6] Add progress indicators for long-running operations
- [ ] T066 [P] [US6] Implement logging throughout the pipeline
- [ ] T067 [P] [US6] Implement retry logic for failed chunks
- [ ] T068 [US6] Create main() function in server/ingest.py
- [ ] T069 [P] [US6] Add command-line arguments for URLs, chunk size, overlap, etc.
- [ ] T070 [P] [US6] Parse configuration file if provided
- [ ] T071 [US6] Write integration tests for full pipeline in server/tests/integration/test_ingestion_pipeline.py

## Phase 9: API Implementation

**Goal**: Create API endpoints for managing the ingestion pipeline

- [ ] T072 Create ingestion API in server/src/api/ingestion_api.py
- [ ] T073 [P] Implement POST /api/v1/ingest-urls endpoint
- [ ] T074 [P] Implement GET /api/v1/ingest-urls/{job_id} endpoint
- [ ] T075 [P] Implement POST /api/v1/bulk-ingest endpoint
- [ ] T076 [P] Implement DELETE /api/v1/ingest-urls/{job_id} endpoint
- [ ] T077 [P] Add authentication and rate limiting to API endpoints
- [ ] T078 [P] Add request validation for API endpoints
- [ ] T079 Write contract tests for API endpoints in server/tests/contract/test_api_contracts.py

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Add finishing touches and ensure quality

- [ ] T080 Add comprehensive error handling throughout the application
- [ ] T081 Implement proper logging with different log levels
- [ ] T082 Add configuration validation and defaults
- [ ] T083 Create README.md with setup and usage instructions
- [ ] T084 Add type hints to all functions and classes
- [ ] T085 Perform code review and refactoring as needed
- [ ] T086 Run full test suite to ensure all components work together
- [ ] T087 Document any remaining implementation details in the codebase