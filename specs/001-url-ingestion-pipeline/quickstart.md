# Quickstart Guide: URL Ingestion & Embedding Pipeline

**Feature**: URL Ingestion & Embedding Pipeline | **Date**: 2025-12-24 | **Branch**: `001-url-ingestion-pipeline`

## Overview

This guide provides instructions for setting up and running the URL ingestion pipeline that fetches content from URLs, cleans and chunks the text, generates embeddings using Cohere models, and stores embeddings and metadata in Qdrant Cloud.

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
python ingest.py --urls "https://example.com/article1" "https://example.com/article2" --chunk-size 800 --overlap 100
```

**Options**:
- `--urls`: Space-separated list of URLs to process
- `--chunk-size`: Target size for text chunks in tokens (default: 800)
- `--overlap`: Overlap between chunks in tokens (default: 100)
- `--force-reprocess`: Re-process content even if previously processed (default: False)

### 2. Using the Main Function

You can also run the ingestion pipeline programmatically by calling the main function:

```python
from ingest import main

urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]

main(urls, chunk_size=800, overlap=100, force_reprocess=False)
```

### 3. Using the API

Start the server:

```bash
cd server
python main.py
```

Submit an ingestion job via API:

```bash
curl -X POST http://localhost:8000/api/v1/ingest-urls \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "urls": [
      "https://example.com/article1",
      "https://example.com/article2"
    ],
    "options": {
      "force_reprocess": false,
      "chunk_size": 800,
      "overlap": 100
    }
  }'
```

## Configuration File

For more complex ingestion tasks, you can create a configuration file:

```yaml
# config.yaml
urls:
  - https://example.com/article1
  - https://example.com/article2
settings:
  chunk_size: 600
  overlap: 100
  model: embed-english-v3.0
  metadata:
    source_type: documentation
    tags:
      - tutorial
      - python
```

Then run:

```bash
python ingest.py --config config.yaml
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

4. **URL Fetching Problems**: If content is not fetching properly, verify that the URLs are accessible and not blocked by robots.txt.

### Enable Debug Logging

Add the following to your `.env` file:

```bash
LOG_LEVEL=DEBUG
```

## Next Steps

1. Integrate with the RAG search API
2. Connect to the chatbot agent
3. Set up monitoring and alerting for the ingestion pipeline