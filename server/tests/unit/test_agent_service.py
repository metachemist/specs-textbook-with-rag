import pytest
from unittest.mock import patch, MagicMock
from agent_service import generate_agent_response


class TestAgentService:
    """
    Unit tests for the agent service functions.
    """

    @patch('agent_service.client')
    @patch('agent_service.search_knowledge_base')
    def test_generate_agent_response_with_tool_call_success(self, mock_search_kb, mock_openai_client):
        """
        Test that generate_agent_response works correctly when the agent calls the tool.
        """
        # Mock the OpenAI client response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_tool_call = MagicMock()
        
        # Set up the tool call
        mock_tool_call.function.name = "search_knowledge_base"
        mock_tool_call.function.arguments = '{"query": "test query"}'
        mock_tool_call.id = "call_123"
        
        mock_message.tool_calls = [mock_tool_call]
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_second_response = MagicMock()
        mock_second_choice = MagicMock()
        mock_second_message = MagicMock()
        mock_second_message.content = "This is the final answer based on the retrieved context."
        mock_second_choice.message = mock_second_message
        mock_second_response.choices = [mock_second_choice]
        
        # Configure the mock client to return our mock responses
        mock_openai_client.chat.completions.create.side_effect = [mock_response, mock_second_response]
        
        # Mock the search_knowledge_base function
        mock_search_result = {
            "success": True,
            "data": MagicMock(),
            "message": "Successfully retrieved results"
        }
        # Create a mock chunk
        mock_chunk = MagicMock()
        mock_chunk.source_file_path = "/docs/test.md"
        mock_chunk.source_url = "https://example.com/docs/test"
        mock_chunk.content = "This is test content for the chunk."
        mock_chunk.score = 0.95
        mock_search_result["data"].chunks = [mock_chunk]
        
        mock_search_kb.return_value = mock_search_result

        # Call the function
        result = generate_agent_response("What is a test?")

        # Assertions
        assert result["status"] == "success"
        assert result["content"] == "This is the final answer based on the retrieved context."
        assert "search_knowledge_base" in result["tool_calls"]
        assert len(result["citations"]) == 1
        assert result["citations"][0]["source_file_path"] == "/docs/test.md"

    @patch('agent_service.client')
    def test_generate_agent_response_no_tool_call(self, mock_openai_client):
        """
        Test that generate_agent_response works correctly when no tool is called.
        """
        # Mock the OpenAI client response without tool calls
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.tool_calls = None
        mock_message.content = "This is a direct response without using the knowledge base."
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        # Configure the mock client to return our mock response
        mock_openai_client.chat.completions.create.return_value = mock_response

        # Call the function
        result = generate_agent_response("Hello, how are you?")

        # Assertions
        assert result["status"] == "success"
        assert result["content"] == "This is a direct response without using the knowledge base."
        assert result["tool_calls"] == []
        assert result["citations"] == []

    @patch('agent_service.client')
    def test_generate_agent_response_error_handling(self, mock_openai_client):
        """
        Test that generate_agent_response handles errors gracefully.
        """
        # Configure the mock client to raise an exception
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")

        # Call the function
        result = generate_agent_response("What is a test?")

        # Assertions
        assert result["status"] == "error"
        assert "error" in result["content"].lower()