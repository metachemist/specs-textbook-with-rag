# Research Document: RAG Agent with OpenAI Tool Use

**Feature**: RAG Agent with OpenAI Tool Use | **Date**: 2025-12-25 | **Branch**: `004-rag-agent-openai-tool`

## Overview

This document captures research findings and technical decisions for implementing the RAG Agent with OpenAI Tool Use that defines a retrieval tool function, implements agent logic using OpenAI Chat Completions API with tools definitions, configures the AI to act as a "Textbook Assistant" that answers strictly based on retrieved context, implements citation logic to mention source chapters/files, and creates a standalone test script to validate the complete workflow.

## Research Findings

### 1. OpenAI Tool Definition Structure

**Decision**: Use JSON Schema to define the retrieval tool for OpenAI's function calling

**Rationale**:
- OpenAI's `tools` parameter requires properly formatted JSON Schema definitions
- Allows the model to understand when and how to call the function
- Enables proper parameter validation and type checking
- Follows OpenAI's recommended approach for function calling

**Implementation approach**:
- Define the retrieval tool with name, description, and parameters
- Use JSON Schema to specify the search query parameter
- Include proper descriptions for model understanding
- Validate the schema before sending to OpenAI API

**Alternatives considered**:
- Direct function calls: Would not leverage OpenAI's function calling capabilities
- Custom tool format: Would not be compatible with OpenAI's system

### 2. Agent Interaction Pattern

**Decision**: Implement a multi-step agent interaction pattern with tool calling and response synthesis

**Rationale**:
- Allows the agent to make informed decisions about when to retrieve information
- Enables proper handling of tool responses and integration into final answer
- Supports the fallback mechanism when no results are found
- Maintains context between tool calls and final response generation

**Implementation approach**:
- Send initial request with system prompt and user query
- Check if the response includes a tool call
- Execute the tool call and retrieve context
- Send the context back to the model for final response synthesis
- Handle cases where no tool call is made or no results are found

**Alternatives considered**:
- Single-step approach: Would not allow for proper context retrieval and synthesis
- Pre-retrieval approach: Would not be efficient as the agent might not need the context

### 3. System Prompt Engineering

**Decision**: Create a comprehensive system prompt that guides the agent's behavior as a "Textbook Assistant"

**Rationale**:
- Properly guides the agent to use only retrieved context
- Ensures citations are included in responses
- Provides clear instructions for fallback scenarios
- Maintains consistency in the agent's responses

**Implementation approach**:
- Define clear role for the agent as a "Textbook Assistant"
- Specify that responses must be based strictly on retrieved context
- Include instructions for citing sources
- Add fallback instructions when no relevant information is found
- Test different prompt variations for optimal results

**Alternatives considered**:
- Generic assistant prompt: Would not ensure proper textbook-based responses
- No system prompt: Would result in inconsistent and potentially inaccurate responses

### 4. Citation Format and Logic

**Decision**: Implement structured citation logic that extracts and formats source information from retrieved context

**Rationale**:
- Ensures proper academic integrity in responses
- Provides users with source information for verification
- Maintains consistency in how sources are presented
- Follows academic citation standards

**Implementation approach**:
- Extract source information (file path, chapter, etc.) from retrieved context
- Format citations in a consistent, readable format
- Integrate citations naturally into the agent's response
- Handle cases where multiple sources are used in a single response

**Alternatives considered**:
- No citations: Would violate academic integrity requirements
- Inconsistent citation formats: Would reduce usability and credibility

### 5. Error Handling and Fallback Strategy

**Decision**: Implement comprehensive error handling with appropriate fallback responses

**Rationale**:
- Ensures the system remains robust when APIs are unavailable
- Provides appropriate user feedback when no results are found
- Maintains good user experience during error conditions
- Follows best practices for API integration

**Implementation approach**:
- Wrap OpenAI API calls in try-catch blocks
- Implement fallback responses when retrieval tool returns no results
- Handle API rate limits and retry logic where appropriate
- Log errors for observability and debugging

**Alternatives considered**:
- Minimal error handling: Would result in poor user experience
- Generic error messages: Would not provide helpful feedback to users

## Technical Unknowns Resolved

1. **Tool definition format**: Resolved to use OpenAI's JSON Schema format for function definitions
2. **Agent interaction pattern**: Resolved to implement a multi-step pattern with tool calling and response synthesis
3. **System prompt structure**: Resolved to create a comprehensive prompt guiding textbook-based responses
4. **Citation implementation**: Resolved to extract and format source information from retrieved context
5. **Error handling approach**: Resolved to implement comprehensive error handling with fallback responses

## Dependencies to Install

```txt
openai>=1.3.5
python-dotenv>=1.0.0
pydantic>=2.5.0
qdrant-client>=1.9.0
pytest>=7.0
```

## Environment Variables Required

```bash
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key (from previous spec)
QDRANT_URL=your_qdrant_cluster_url (from previous spec)
QDRANT_API_KEY=your_qdrant_api_key (from previous spec)
LOG_LEVEL=INFO
```

## API Rate Limits and Constraints

- OpenAI API: Check current rate limits (requests/minute and tokens/minute)
- Token limits: Consider context window limits when formatting responses
- Implement backoff strategies for API calls
- Monitor costs associated with API usage