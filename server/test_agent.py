#!/usr/bin/env python3
"""
Standalone validation script for the RAG Agent with OpenAI Tool Use.
Tests the agent's ability to call the retrieval tool and generate sourced answers.
"""

from agent_service import generate_agent_response


def main():
    """
    Main function to run the validation script.
    Asks a sample question and verifies the agent's behavior.
    """
    print("Starting RAG Agent validation...")

    # Sample question for validation
    sample_question = "What is a sensor in robotics?"

    print(f"Querying: '{sample_question}'")

    # Generate response using the agent
    response = generate_agent_response(sample_question)

    # Print the results
    print("\nAgent Response:")
    print(f"Content: {response.get('content', 'No content returned')}")
    print(f"Status: {response.get('status', 'unknown')}")
    print(f"Tool calls: {response.get('tool_calls', [])}")

    # Print citations if any
    citations = response.get('citations', [])
    if citations:
        print(f"\nCitations ({len(citations)} found):")
        for i, citation in enumerate(citations, 1):
            print(f"  {i}. Source: {citation.get('source_file_path', 'N/A')}")
            print(f"     Preview: {citation.get('text_preview', 'N/A')[:100]}...")
    else:
        print("\nNo citations found in response.")

    # Verification steps
    print("\nVerification:")
    tool_calls = response.get('tool_calls', [])
    if 'search_knowledge_base' in tool_calls:
        print("SUCCESS: Tool was called successfully")
    else:
        print("WARNING: Tool was not called")

    if citations:
        print("SUCCESS: Citations were included in the response")
    else:
        print("WARNING: No citations found in the response")

    print("\nValidation completed.")


if __name__ == "__main__":
    main()