#!/usr/bin/env python3
"""
Standalone validation script for the RAG retrieval pipeline.
Performs a "sanity check" query and prints raw search results to the console.
"""

from rag_service import search_knowledge_base


def main():
    """
    Main function to run the validation script.
    Performs a sample query and prints the raw search results to the console.
    """
    print("Starting RAG retrieval validation...")
    
    # Sample query for validation
    sample_query = "What is a node?"
    
    print(f"Querying: '{sample_query}'")
    
    # Perform the search
    result = search_knowledge_base(sample_query)
    
    if result["success"]:
        print("Search completed successfully")

        # Print raw search results (score + payload) to the console
        print("\nRaw search results:")
        print("-" * 50)
        
        if "data" in result and hasattr(result["data"], "chunks"):
            for i, chunk in enumerate(result["data"].chunks):
                print(f"Result #{i+1}:")
                print(f"  Score: {chunk.score}")
                print(f"  Content Preview: {chunk.content[:100]}...")
                print(f"  Source URL: {chunk.source_url}")
                print(f"  Source File Path: {chunk.source_file_path}")
                print(f"  Chunk Index: {chunk.chunk_index}")
                print(f"  Metadata: {chunk.metadata}")
                print("-" * 30)
        else:
            print("No results returned from the search.")
            
        print(f"\nTotal results found: {len(result['data'].chunks) if 'data' in result and hasattr(result['data'], 'chunks') else 0}")
    else:
        print(f"Search failed: {result['message']}")
        if "error" in result:
            print(f"Error details: {result['error']}")


if __name__ == "__main__":
    main()