# Quickstart Guide: RAG Ingestion Pipeline

**Feature**: RAG Ingestion Pipeline | **Date**: 2025-12-24 | **Branch**: `002-rag-ingestion-pipeline`

## Overview

This guide provides instructions for setting up and running the RAG ingestion pipeline that reads markdown content from the `/web` directory, chunks it appropriately for technical textbook content, generates embeddings using the Cohere API, and stores them in Qdrant vector database with metadata.

## Prerequisites

- Python 3.10 or higher
- Git
- Access to Cohere API (API key)
- Access to Qdrant Cloud (URL and API key)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the server directory with the following content:

```bash
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Running the Ingestion Pipeline

### 1. Direct Script Execution

```bash
cd server
python ingest.py --source-path ../web/docs --chunk-size 800 --overlap 100
```

**Options**:
- `--source-path`: Path to the directory containing markdown files (default: `../web/docs`)
- `--chunk-size`: Target size for text chunks in tokens (default: 800)
- `--overlap`: Overlap between chunks in tokens (default: 100)
- `--force-reprocess`: Re-process documents even if unchanged (default: False)

### 2. Using the API

Start the server:

```bash
cd server
python main.py
```

Submit an ingestion job via API:

```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "source_path": "/web/docs",
    "options": {
      "force_reprocess": false,
      "chunk_size": 800,
      "overlap": 100
    }
  }'
```

## Verification

### 1. Run Verification Script

```bash
cd server
python -c "from src.services.verification_service import verify_indexing; verify_indexing()"
```

### 2. Check API

```bash
curl -X GET http://localhost:8000/api/v1/verify \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Testing

### Run Unit Tests

```bash
cd server
pytest tests/unit/ -v
```

### Run Integration Tests

```bash
cd server
pytest tests/integration/ -v
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Verify that your Cohere and Qdrant API keys are correct and have sufficient permissions.

2. **Rate Limiting**: If you encounter rate limit errors, implement appropriate delays or upgrade your API plan.

3. **Memory Issues**: For large documents, consider reducing the batch size for embedding generation.

4. **Chunking Problems**: If content is not chunking properly, verify that your markdown files are properly formatted.

### Enable Debug Logging

Add the following to your `.env` file:

```bash
LOG_LEVEL=DEBUG
```

## Next Steps

1. Integrate with the RAG search API (Spec 2)
2. Connect to the chatbot agent (Spec 3)
3. Set up monitoring and alerting for the ingestion pipeline