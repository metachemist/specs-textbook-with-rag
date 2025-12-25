# Quickstart Guide: Frontend Chat Widget Integration

**Feature**: Frontend Chat Widget Integration | **Date**: 2025-12-25 | **Branch**: `005-frontend-chat-widget`

## Overview

This guide provides instructions for setting up and using the Frontend Chat Widget Integration that enables students to interact with the AI assistant directly from any page in the textbook website. The implementation includes configuring CORS on the FastAPI backend, creating a React ChatWidget component, and globally embedding it in the Docusaurus layout.

## Prerequisites

- Node.js 16+ and npm/yarn for frontend development
- Python 3.10+ for backend development
- Git
- Access to OpenAI API (API key) - from previous spec
- Access to Cohere API (API key) - from previous spec
- Access to Qdrant Cloud (URL and API key) - from previous spec

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup

```bash
cd server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd web
npm install
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

## Backend Configuration

### 1. Configure CORS in FastAPI

Update `server/main.py` to include CORS middleware:

```python
from fastapi.middleware.cors import CORSMiddleware

# Add CORS middleware to allow requests from Docusaurus frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Start the Backend Server

```bash
cd server
python main.py
```

The backend will start on `http://localhost:8000`.

## Frontend Integration

### 1. Create the Chat Widget Component

The ChatWidget component is located at `web/src/components/ChatWidget/ChatWidget.js` and includes:

- A floating chat button that appears on all pages
- A chat window with input box and message list
- Logic to POST user messages to the backend API
- Markdown rendering for AI responses

### 2. Embed the Widget Globally

The widget is embedded globally by wrapping the Root component in Docusaurus at `web/src/theme/Root.js`.

### 3. Start the Frontend Server

```bash
cd web
npm run start
```

The frontend will start on `http://localhost:3000`.

## Using the Chat Widget

### 1. Accessing the Widget

- The floating chat button appears on all pages of the textbook website
- Click the button to open the chat window
- The widget maintains its state as you navigate between pages

### 2. Sending Messages

- Type your message in the input box
- Press Enter or click the send button
- Your message appears in the message list with a loading indicator
- The AI response will appear once processed

### 3. Viewing Responses

- AI responses are displayed with proper markdown formatting
- Source citations are shown when available
- Loading indicators are shown while waiting for responses

## Testing

### Frontend Component Tests

```bash
cd web
npm test
```

### Backend API Tests

```bash
cd server
pytest tests/unit/ -v
```

### Integration Tests

```bash
cd server
pytest tests/integration/ -v
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Verify that the backend has CORS configured to allow requests from `http://localhost:3000`.

2. **API Connection Errors**: Verify that your API keys are correct and have sufficient permissions.

3. **Widget Not Appearing**: Check that the Root.js component properly wraps the application with the ChatWidget.

4. **Messages Not Sending**: Verify that the backend server is running and the API endpoint is accessible.

### Enable Debug Logging

Add the following to your `.env` file:

```bash
LOG_LEVEL=DEBUG
```

## Next Steps

1. Deploy the backend to a production environment (Railway/Render)
2. Deploy the frontend to a hosting platform (GitHub Pages, Vercel, etc.)
3. Update CORS settings for production domains
4. Implement additional chat features as needed