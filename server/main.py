import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from qdrant_client import QdrantClient
import psycopg2
from src.api import chat_router, personalize_router
from src.api.ingestion_api import router as ingestion_router
from src.api.retrieval_api import router as retrieval_router, add_rate_limit_handler
import logging

# Import the RAG service
from rag_service import initialize_clients, search_context, generate_answer


# Request/Response models
class ChatRequest(BaseModel):
    message: str

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="Backend API for the AI-Native Textbook with RAG Platform",
    version="1.0.0",
)

# Global variables for clients
openai_client = None
qdrant_client = None
neon_conn = None


@app.on_event("startup")
def startup_event():
    """Initialize API clients on startup"""
    global openai_client, qdrant_client, neon_conn

    print("Initializing API clients...")

    # Initialize OpenAI client
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai_client = OpenAI(api_key=openai_api_key)
            print("✅ Connected to OpenAI")
        else:
            print("❌ OpenAI API key not found")
    except Exception as e:
        print(f"❌ Failed to connect to OpenAI: {e}")

    # Initialize Qdrant client
    try:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url and qdrant_api_key:
            qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            # Test connection
            qdrant_client.get_collections()
            print("✅ Connected to Qdrant")
        elif qdrant_url:
            qdrant_client = QdrantClient(url=qdrant_url)
            # Test connection
            qdrant_client.get_collections()
            print("✅ Connected to Qdrant (no API key)")
        else:
            print("❌ Qdrant URL not found")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")

    # Connect to Neon database
    try:
        neon_db_url = os.getenv("NEON_DATABASE_URL")
        if neon_db_url:
            neon_conn = psycopg2.connect(neon_db_url)
            print("✅ Connected to Neon Database")
        else:
            print("❌ Neon Database URL not found")
    except Exception as e:
        print(f"❌ Failed to connect to Neon Database: {e}")

    # Initialize the RAG service with the clients
    try:
        initialize_clients(openai_client, qdrant_client)
        print("✅ RAG service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")



@app.on_event("shutdown")
def shutdown_event():
    """Clean up resources on shutdown"""
    global neon_conn
    if neon_conn:
        neon_conn.close()
        print("Closed connection to Neon Database")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat_router)
app.include_router(personalize_router)
app.include_router(ingestion_router)
app.include_router(retrieval_router)

# Add rate limit handler
add_rate_limit_handler(app)

@app.get("/")
def read_root():
    # Check the status of all services
    openai_status = "ready" if openai_client else "not configured"
    qdrant_status = "ready" if qdrant_client else "not configured"
    db_status = "connected" if neon_conn else "not connected"

    return {
        "message": "Physical AI & Humanoid Robotics Textbook API",
        "services": {
            "openai": openai_status,
            "qdrant": qdrant_status,
            "db": db_status
        }
    }


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Handle RAG queries from the textbook interface
    Input: JSON { "message": "What is ROS 2?" }
    Output: JSON { "response": "ROS 2 is...", "sources": ["01-nodes.md"] }
    """
    try:
        # Search for relevant context using the RAG service
        context = search_context(request.message)

        if not context:
            return {
                "response": "I couldn't find relevant information in the textbook to answer your question.",
                "sources": []
            }

        # Generate an answer using the context
        response, sources = generate_answer(request.message, context)

        return {
            "response": response,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
  