# Quickstart Guide: RAG Agent with OpenAI Tool Use

**Feature**: RAG Agent with OpenAI Tool Use | **Date**: 2025-12-25 | **Branch**: `004-rag-agent-openai-tool`

## Overview

This guide provides instructions for setting up and using the RAG Agent with OpenAI Tool Use that defines a retrieval tool function, implements agent logic using OpenAI Chat Completions API with tools definitions, configures the AI to act as a "Textbook Assistant" that answers strictly based on retrieved context, implements citation logic to mention source chapters/files, and creates a standalone test script to validate the complete workflow.

## Prerequisites

- Python 3.10 or higher
- Git
- Access to OpenAI API (API key)
- Access to Cohere API (API key) - from previous spec
- Access to Qdrant Cloud (URL and API key) - from previous spec

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Virtual Environment

```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the server directory with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cluster_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
LOG_LEVEL=INFO
```

## Using the Agent Service

### 1. Direct Module Usage

```python
from agent_service import generate_response

# Generate a response to a user query
user_message = "What is a sensor in robotics?"
response = generate_response(user_message)
print(f"Response: {response['content']}")
print(f"Citations: {response['citations']}")
```

### 2. Using the Validation Script

Run the standalone validation script to perform a sanity check:

```bash
cd server
python test_agent.py
```

This script will:
- Ask a sample question ("What is a sensor?")
- Verify that the agent calls the retrieval tool
- Show the retrieved context
- Display the final agent response with citations

### 3. Using the API

Start the server:

```bash
cd server
python main.py
```

Submit a query via API:

```bash
curl -X POST http://localhost:8000/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "message": "What is a sensor in robotics?",
    "context": {
      "include_citations": true
    }
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

1. **API Connection Errors**: Verify that your OpenAI, Cohere, and Qdrant API keys are correct and have sufficient permissions.

2. **Rate Limiting**: If you encounter rate limit errors, implement appropriate delays or upgrade your API plan.

3. **No Results Found**: If the agent says it doesn't know, verify that relevant content was properly ingested in the previous steps.

4. **Citation Issues**: If citations are missing or incorrect, verify that source information is properly preserved in the retrieval pipeline.

### Enable Debug Logging

Add the following to your `.env` file:

```bash
LOG_LEVEL=DEBUG
```

## Next Steps

1. Integrate with the frontend interface (Spec 4)
2. Set up monitoring and alerting for the agent pipeline
3. Add more sophisticated tool functions as needed