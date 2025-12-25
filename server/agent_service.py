"""
Main Agent service module for the RAG Agent with OpenAI Tool Use.
Provides functions for processing user queries through an AI agent that can call retrieval tools.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
import json

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.warning("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Import the RAG service to use the search functionality
from rag_service import search_knowledge_base

# Define the retrieval tool that the agent can use
retrieval_tool = {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Search the knowledge base for information related to the user's query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information in the knowledge base"
                }
            },
            "required": ["query"]
        }
    }
}

# System prompt for the "Textbook Assistant"
system_prompt = {
    "role": "system",
    "content": """You are a helpful textbook assistant. Answer the user's questions based ONLY on the provided context.
    Do not use any prior knowledge or general information. If the context doesn't contain the information needed to answer the question,
    politely say that you don't have that information in the textbook. Always cite your sources when providing information."""
}

def generate_agent_response(message: str) -> Dict[str, Any]:
    """
    Generate a response to a user message using the AI agent with tool calling capability.

    Args:
        message: The user's query or message to the agent

    Returns:
        Dictionary containing the agent's response, citations, and status
    """
    logger.info(f"Processing agent request: {message[:50]}...")

    # Check if OpenAI client is available
    if client is None:
        logger.error("OpenAI client not available - API key not set")
        return {
            "content": "I'm sorry, but the OpenAI service is not configured properly. Please set the OPENAI_API_KEY environment variable.",
            "citations": [],
            "tool_calls": [],
            "status": "error"
        }

    try:
        # Prepare the messages for the OpenAI API
        messages = [
            system_prompt,
            {"role": "user", "content": message}
        ]

        # Call the OpenAI API with the retrieval tool available
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using the cost-effective model as specified
            messages=messages,
            tools=[retrieval_tool],
            tool_choice="auto"  # Let the model decide when to call the tool
        )

        # Get the response message
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        logger.info(f"OpenAI response received, tool_calls: {bool(tool_calls)}")

        # If the model wants to call the tool
        if tool_calls:
            logger.info(f"Tool calls detected: {[tc.function.name for tc in tool_calls]}")

            # Execute the tool calls
            available_functions = {
                "search_knowledge_base": search_knowledge_base,
            }

            messages.append(response_message)  # Add the assistant's request to call the tool

            # Process each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]

                # Parse the function arguments
                function_args = json.loads(tool_call.function.arguments)
                query = function_args.get("query")

                logger.info(f"Executing tool '{function_name}' with query: {query}")

                # Execute the function
                function_response = function_to_call(query_text=query)

                logger.info(f"Tool execution result: success={function_response.get('success')}")

                # Add the function response to the messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                })

            # Call the API again with the function response to get the final answer
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            final_content = second_response.choices[0].message.content

            logger.info(f"Final response generated, content length: {len(final_content) if final_content else 0}")

            # Extract citations from the function response
            citations = []
            if function_response.get("success") and function_response.get("data"):
                for chunk in function_response["data"].chunks:
                    from src.models.citation import Citation
                    citation = Citation(
                        source_file_path=chunk.source_file_path,
                        source_url=chunk.source_url,
                        text_preview=chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content,
                        confidence_score=chunk.score
                    )
                    citations.append(citation)

            logger.info(f"Response completed with {len(citations)} citations")

            return {
                "content": final_content,
                "citations": [c.dict() for c in citations],
                "tool_calls": [tool_call.function.name for tool_call in tool_calls],
                "status": "success"
            }
        else:
            # If no tool was called, return the direct response
            logger.info("No tool calls required, returning direct response")
            return {
                "content": response_message.content,
                "citations": [],
                "tool_calls": [],
                "status": "success"
            }

    except Exception as e:
        # Handle any errors that occur during the process
        logger.error(f"Error in generate_agent_response: {str(e)}")
        return {
            "content": "I'm sorry, but I encountered an error while processing your request.",
            "citations": [],
            "tool_calls": [],
            "status": "error"
        }