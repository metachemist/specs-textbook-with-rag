# Physical AI & Humanoid Robotics Textbook

An AI-Native Interactive Textbook for Physical AI & Humanoid Robotics, featuring:
- Docusaurus-based interactive textbook covering ROS 2, Gazebo, and NVIDIA Isaac
- Integrated RAG Chatbot that answers student queries using textbook content
- Built with the tech stack mandated by the project constitution

## Tech Stack

- **Frontend**: Docusaurus (React/TypeScript), Tailwind CSS
- **Backend**: FastAPI (Python), Pydantic for validation
- **Database**: Neon (Serverless Postgres) for chat history/user data
- **Vector Search**: Qdrant for RAG (retrieving book context)
- **AI/LLM**: OpenAI Agents or ChatKit for response generation
- **Auth**: Better Auth (optional but preferred)

## Architecture

The project follows a modular architecture with separate directories:
- `/web` - Docusaurus frontend implementation
- `/server` - FastAPI backend implementation
- Each component is designed to be independently testable and maintainable

## Development Workflow

This project adheres to the principles outlined in the project constitution:
- Strict PEP 8 (Python) and Prettier (JS/TS) code style enforcement
- Modular design with clear separation between frontend and backend
- Comprehensive error handling and logging for all external API calls
- Visual documentation using Mermaid.js diagrams