# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

**Feature**: AI-Native Textbook with RAG Platform
**Date**: 2025-12-19

## Overview
This guide provides a quick setup and development workflow for the Physical AI & Humanoid Robotics textbook project.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Python 3.9+ (for backend development)
- Git

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Setup Frontend (Docusaurus)
```bash
# Navigate to web directory
cd web

# Install dependencies
npm install

# Start development server
npm start
```

Your Docusaurus site will be available at `http://localhost:3000`

### 3. Setup Backend (FastAPI)
```bash
# Navigate to server directory
cd server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Your backend API will be available at `http://localhost:8000`

## Project Structure
```
project-root/
├── web/                 # Docusaurus frontend
│   ├── docs/            # Textbook content
│   ├── src/             # Custom components
│   ├── static/          # Static assets
│   └── docusaurus.config.ts
├── server/              # FastAPI backend
│   ├── src/
│   ├── tests/
│   └── requirements.txt
└── specs/               # Feature specifications
    └── 001-textbook-rag-platform/
```

## Key Development Tasks

### Adding New Content
1. Create a new markdown file in the appropriate module directory under `web/docs/`
2. Update `sidebars.ts` to include the new content in the navigation
3. Ensure the content follows the curriculum structure

### Adding Components
1. Create new components in `web/src/components/`
2. Follow the existing patterns for ChatBotWidget, PersonalizeButton, and TranslateButton
3. Ensure components are properly typed with TypeScript

### API Integration
1. Backend endpoints are defined in `server/src/api/`
2. Frontend components make API calls to the backend
3. API contracts are documented in `specs/001-textbook-rag-platform/contracts/`

## Running Tests
```bash
# Frontend tests
cd web
npm test

# Backend tests
cd server
python -m pytest
```

## Building for Production
```bash
# Build frontend
cd web
npm run build

# The built site will be in the build/ directory
```

## Deployment
1. Frontend: Deploy the `web/build` directory to GitHub Pages
2. Backend: Deploy the server to Railway or Render (as specified in the constitution)