# Research Document: Frontend Chat Widget Integration

**Feature**: Frontend Chat Widget Integration | **Date**: 2025-12-25 | **Branch**: `005-frontend-chat-widget`

## Overview

This document captures research findings and technical decisions for implementing the Frontend Chat Widget Integration that enables students to interact with the AI assistant directly from any page in the textbook website. The implementation includes configuring CORS on the FastAPI backend, creating a React ChatWidget component, and globally embedding it in the Docusaurus layout.

## Research Findings

### 1. CORS Configuration for FastAPI

**Decision**: Use `fastapi.middleware.cors.CORSMiddleware` to allow requests from `localhost:3000`

**Rationale**:
- FastAPI provides a built-in middleware specifically for CORS handling
- Easy to configure with allowed origins, methods, and headers
- Secure by default, allowing fine-grained control over cross-origin requests
- Required for local development where frontend runs on port 3000 and backend on port 8000

**Implementation approach**:
- Import and add CORSMiddleware to the FastAPI app
- Configure allowed origins to include `http://localhost:3000`
- Allow credentials, methods, and headers as needed for the chat functionality
- Include proper error handling for CORS failures

**Alternatives considered**:
- Manual CORS headers: Would be error-prone and less secure
- Proxy server: Would add unnecessary complexity for this use case

### 2. React Component Architecture

**Decision**: Implement the ChatWidget as a React component with separate sub-components for different UI elements

**Rationale**:
- Separation of concerns improves maintainability and testability
- Reusable components can be used in different contexts if needed
- Clear state management for messages, loading states, and widget visibility
- Follows React best practices for component composition

**Implementation approach**:
- Create a main ChatWidget component to manage overall state
- Create sub-components for ChatButton, ChatWindow, and MessageList
- Use React hooks (useState, useEffect) for state management
- Implement proper event handling for user interactions
- Use CSS modules for styling to avoid global CSS conflicts

**Alternatives considered**:
- Single monolithic component: Would be harder to maintain and test
- External state management (Redux): Would add unnecessary complexity for this feature

### 3. Global Embedding Strategy for Docusaurus

**Decision**: Wrap the Docusaurus Root component to globally embed the chat widget

**Rationale**:
- Docusaurus provides a mechanism to wrap the entire app with custom components
- Ensures the chat widget appears on every page without modifying each page individually
- Clean approach that follows Docusaurus conventions
- Preserves widget state across page navigations (until refresh)

**Implementation approach**:
- Create a Root.js file in the theme directory
- Import and render the ChatWidget component within the Root wrapper
- Ensure the widget is properly positioned and styled globally
- Test that the widget appears correctly on all page types (docs, blog, etc.)

**Alternatives considered**:
- Modifying Layout component: Would be more invasive and potentially conflict with Docusaurus updates
- Adding to each page individually: Would be repetitive and error-prone

### 4. State Management Strategy

**Decision**: Use React's built-in useState and useEffect hooks for state management

**Rationale**:
- Simple and lightweight for the scope of this component
- No external dependencies required
- Built-in React functionality that team is familiar with
- Sufficient for managing messages, loading state, and widget visibility

**Implementation approach**:
- Use useState for managing messages array, loading state, and widget open/closed state
- Use useEffect for handling API calls and cleanup
- Implement proper error handling and state updates
- Consider performance implications of re-renders

**Alternatives considered**:
- Redux or Context API: Would add unnecessary complexity for this simple state
- External libraries like Zustand: Would add dependencies without significant benefits

### 5. API Communication and Error Handling

**Decision**: Use the browser's fetch API with async/await for API communication with comprehensive error handling

**Rationale**:
- Fetch API is built into modern browsers, no external dependencies needed
- Async/await provides clean, readable code for asynchronous operations
- Proper error handling ensures good user experience when backend is unavailable
- Timeout handling prevents hanging requests

**Implementation approach**:
- Implement fetch calls to the backend API endpoint
- Add proper request headers (Content-Type, etc.)
- Handle different response types (success, error, network failure)
- Implement loading states and timeout mechanisms
- Provide user-friendly error messages for different failure scenarios

**Alternatives considered**:
- Axios: Would add an external dependency without significant benefits
- Other HTTP libraries: Would add unnecessary complexity

## Technical Unknowns Resolved

1. **CORS configuration**: Resolved to use FastAPI's built-in CORSMiddleware
2. **Component architecture**: Resolved to use a modular approach with separate sub-components
3. **Global embedding**: Resolved to use Docusaurus's Root component wrapping
4. **State management**: Resolved to use React's built-in hooks
5. **API communication**: Resolved to use fetch API with proper error handling

## Dependencies to Install

```txt
# Frontend (web/package.json)
react-markdown
remark-gfm
rehype-raw

# Backend (server/requirements.txt)
python-multipart
```

## Environment Variables Required

```bash
# For local development
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

## API Endpoints to Integrate With

- POST `/api/chat` - Send user message and receive AI response
- Expected request format: `{ "message": "user's message" }`
- Expected response format: `{ "response": "AI's response", "sources": ["source files"] }`