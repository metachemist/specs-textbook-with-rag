import os
from typing import List, Dict, Tuple
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging

# Initialize clients (these will be set from main.py)
openai_client = None
qdrant_client = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def embed_text(text: str) -> List[float]:
    """
    Uses OpenAI text-embedding-3-small to convert text to vectors.
    """
    global openai_client
    
    if not openai_client:
        raise Exception("OpenAI client not initialized")
    
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error embedding text: {e}")
        raise e

def search_context(query: str, limit: int = 5) -> List[Dict]:
    """
    Searches Qdrant for the most relevant textbook chunks.
    """
    global qdrant_client
    
    if not qdrant_client:
        raise Exception("Qdrant client not initialized")
    
    try:
        # Embed the query
        query_vector = embed_text(query)
        
        # Search in the textbook_knowledge collection
        search_results = qdrant_client.search(
            collection_name="textbook_knowledge",
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        
        # Extract relevant information from results
        contexts = []
        for result in search_results:
            contexts.append({
                "content": result.payload.get("content", ""),
                "source": result.payload.get("source", ""),
                "title": result.payload.get("title", ""),
                "score": result.score
            })
        
        return contexts
    except Exception as e:
        logger.error(f"Error searching context: {e}")
        raise e

def generate_answer(query: str, context: List[Dict]) -> Tuple[str, List[str]]:
    """
    Sends the user query + context to GPT-4o-mini to get a grounded answer.
    Returns the answer and list of sources.
    """
    global openai_client
    
    if not openai_client:
        raise Exception("OpenAI client not initialized")
    
    try:
        # Format the context for the prompt
        context_str = "\n\n".join([f"Source: {item['source']}\nContent: {item['content']}" for item in context])
        
        # Create the prompt
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics Textbook. 
        Answer the user's question based on the provided textbook content.
        
        Context from textbook:
        {context_str}
        
        User's question: {query}
        
        Please provide a helpful answer based on the textbook content and mention which sources you used.
        If the context doesn't contain relevant information to answer the question, say so.
        """
        
        # Call the OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini as requested
            messages=[
                {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics Textbook. Provide helpful answers based on the textbook content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # Extract sources from the context
        sources = list(set([item["source"] for item in context if item["source"]]))  # Remove duplicates
        
        return answer, sources
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise e

def initialize_clients(openai_cl, qdrant_cl):
    """
    Initialize the global clients with provided instances
    """
    global openai_client, qdrant_client
    openai_client = openai_cl
    qdrant_client = qdrant_cl