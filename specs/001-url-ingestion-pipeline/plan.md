# Implementation Plan: URL Ingestion & Embedding Pipeline

**Branch**: `001-url-ingestion-pipeline` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-url-ingestion-pipeline/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a URL ingestion pipeline that fetches content from URLs, cleans and chunks the text, generates embeddings using Cohere models, and stores embeddings and metadata in Qdrant Cloud. The implementation will be added to the existing `server/` folder with a main function to run the full pipeline end-to-end.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv, PyYAML, tiktoken
**Storage**: Qdrant Cloud vector database with metadata storage
**Testing**: pytest with unit and integration tests for ingestion pipeline
**Target Platform**: Linux server (deployable to Railway/Render)
**Project Type**: backend service
**Performance Goals**: Process 100 URLs within 2 hours, achieve 99% success rate during peak API usage
**Constraints**: Embedding service rate limits, vector storage limits, <100MB memory for chunking operations
**Scale/Scope**: Handle up to 10,000+ URLs, support multiple concurrent ingestion jobs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tech Stack Adherence: Uses Qdrant as mandated in constitution, Python for backend services, follows library-first approach
- Architecture Compliance: Separate /server directory for backend services, adheres to modular architecture
- Agentic Workflow: Will follow PEP 8, include error handling for external API calls (Cohere, Qdrant), and include Mermaid.js diagrams
- Testing Requirements: Test-first approach with pytest for unit and integration tests of the ingestion pipeline
- Observability: Will include structured logging for Cohere and Qdrant API calls, error handling with user-friendly messages

## Project Structure

### Documentation (this feature)

```text
specs/001-url-ingestion-pipeline/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application: Docusaurus frontend + FastAPI backend
web/
├── docs/
├── src/
│   ├── components/
│   ├── pages/
│   └── css/
├── static/
└── docusaurus.config.js

server/
├── src/
│   ├── models/
│   │   ├── url_content.py
│   │   ├── clean_text.py
│   │   ├── text_chunk.py
│   │   ├── embedding.py
│   │   └── metadata.py
│   ├── services/
│   │   ├── url_fetch_service.py
│   │   ├── text_cleaning_service.py
│   │   ├── chunking_service.py
│   │   ├── embedding_service.py
│   │   └── storage_service.py
│   ├── api/
│   │   └── ingestion_api.py
│   ├── utils/
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── logger.py
│   └── config/
│       └── settings.py
├── tests/
│   ├── unit/
│   │   ├── test_url_fetch_service.py
│   │   ├── test_text_cleaning_service.py
│   │   ├── test_chunking_service.py
│   │   ├── test_embedding_service.py
│   │   └── test_storage_service.py
│   ├── integration/
│   │   └── test_ingestion_pipeline.py
│   └── contract/
│       └── test_api_contracts.py
├── requirements.txt
├── .env.example
├── .env
└── ingest.py            # Main ingestion script with main() function
```

**Structure Decision**: Following the mandated architecture of separate /web and /server directories to ensure modularity and adherence to agentic workflow rules. The ingestion service will be implemented as a standalone library with clear interfaces.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | (None) | (None) |
