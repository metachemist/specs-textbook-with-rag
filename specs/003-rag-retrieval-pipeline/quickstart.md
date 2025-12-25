# Quickstart Guide: RAG Retrieval & Validation Pipeline

**Feature**: RAG Retrieval & Validation Pipeline | **Date**: 2025-12-24 | **Branch**: `003-rag-retrieval-pipeline`

## Overview

This guide provides instructions for setting up and using the RAG retrieval pipeline that accepts text queries, converts them to vector embeddings using Cohere, performs cosine similarity search in Qdrant Cloud, and returns the most relevant text chunks with metadata.

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

## Using the RAG Service

### 1. Direct Module Usage

```python
from rag_service import get_embedding, search_knowledge_base

# Get embedding for a text query
query_text = "What is a node?"
query_embedding = get_embedding(query_text)

# Search the knowledge base
results = search_knowledge_base(query_text)
print(f"Found {len(results)} relevant chunks")
for chunk in results:
    print(f"Score: {chunk['score']}")
    print(f"Content: {chunk['content'][:100]}...")
    print(f"Source: {chunk['metadata']['source_url']}")
```

### 2. Using the Validation Script

Run the standalone validation script to perform a sanity check:

```bash
cd server
python test_retrieval.py
```

This script will:
- Perform a sample query ("What is a node?")
- Print raw search results (score + payload) to the console
- Verify that the retrieval pipeline is working correctly

### 3. Using the API

Start the server:

```bash
cd server
python main.py
```

Submit a search query via API:

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "query": "What is a node?",
    "top_k": 5
  }'
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

3. **No Results Found**: If search returns no results, verify that content was properly ingested in the previous step (Spec 1).

4. **Performance Issues**: If search latency is high, verify that Qdrant is properly configured with appropriate indexes.

### Enable Debug Logging

Add the following to your `.env` file:

```bash
LOG_LEVEL=DEBUG
```

## Next Steps

1. Integrate with the generative answer component (Spec 3)
2. Connect to the frontend interface (Spec 4)
3. Set up monitoring and alerting for the retrieval pipeline