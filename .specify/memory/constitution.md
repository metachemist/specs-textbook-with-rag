<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.0.0
Modified principles: None (new constitution)
Added sections: All sections (new constitution)
Removed sections: None
Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Runtime docs requiring updates: ✅ updated - README.md
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Library-First Approach
Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries. Each component (backend services, frontend modules, RAG pipeline) must be modular and reusable.

### II. Agentic Workflow Discipline
Strict adherence to predefined workflow rules: Code Style (PEP 8 for Python, Prettier for JS/TS), Modularity (separate /server and /web directories), Error Handling (try/catch blocks and logging for all external API calls), and Visual Documentation (Mermaid.js diagrams for complex logic).

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced. Backend API tests, frontend component tests, and RAG pipeline tests must be written before implementation.

### IV. Integration Testing
Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication (Docusaurus-FastAPI connection), Shared schemas (Pydantic models), and RAG pipeline end-to-end flows.

### V. Observability & Error Handling
Structured logging required for all external API calls (OpenAI, Qdrant, Neon DB); Comprehensive error handling with user-friendly messages; Metrics collection for RAG performance and chat response times.

### VI. Tech Stack Adherence
Strict enforcement of predetermined technology stack: Docusaurus (React/TypeScript), Tailwind CSS (frontend), FastAPI (Python), Pydantic (validation), Neon (PostgreSQL), Qdrant (vector search), OpenAI Agents/ChatKit (AI/LLM), Better Auth (authentication).

## Architecture & Implementation Standards

### Frontend Requirements
Docusaurus-based interactive textbook with responsive design using Tailwind CSS; Interactive elements for enhanced learning; Integration with RAG chatbot widget; Chapter navigation and search functionality.

### Backend Requirements
FastAPI-based service with Pydantic validation for all data models; RESTful API design with proper status codes; Async support for handling concurrent requests; Comprehensive API documentation via Swagger/OpenAPI.

### RAG Pipeline Standards
Qdrant vector database for storing textbook content embeddings; Retrieval-augmented generation for contextual responses; Chunking strategy for optimal context retrieval; Semantic search capabilities.

### Deployment & Infrastructure
Separate deployment pipelines: GitHub Pages for frontend (Docusaurus), Railway/Render for backend (FastAPI); Environment variable management for secrets; CI/CD workflows for automated testing and deployment.

## Development Workflow & Quality Assurance

### Phase-Based Development
Adherence to four-phase roadmap: Phase 1 (Docusaurus setup & chapter generation), Phase 2 (FastAPI + Qdrant + RAG implementation), Phase 3 (Chat widget integration), Phase 4 (Deployment).

### Code Quality Gates
Static analysis tools (flake8, mypy, eslint) must pass before merging; All external API calls must have error handling; Frontend components must be properly typed with TypeScript interfaces.

### Review Process
Peer code reviews required for all pull requests; Architecture compliance verification; Performance benchmarks for RAG pipeline; Security review for user data handling.

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, and migration plan; All PRs/reviews must verify compliance with tech stack and architecture decisions; Complexity must be justified with clear benefits to the learning experience.

**Version**: 1.0.0 | **Ratified**: 2025-12-19 | **Last Amended**: 2025-12-19