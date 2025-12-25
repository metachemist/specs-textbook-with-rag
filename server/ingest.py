#!/usr/bin/env python3
"""
Main ingestion script for the URL Ingestion & Embedding Pipeline.

This script fetches content from URLs, cleans and chunks the text,
generates embeddings using Cohere models, and stores embeddings and 
metadata in Qdrant Cloud.
"""

import argparse
import sys
from typing import List
from src.services.ingestion_pipeline import IngestionPipeline


def main(urls: List[str], 
         chunk_size: int = 800, 
         overlap: int = 100, 
         force_reprocess: bool = False) -> int:
    """
    Main function to run the full ingestion pipeline end-to-end.
    
    Args:
        urls: List of URLs to process
        chunk_size: Target size for text chunks in tokens
        overlap: Overlap between chunks in tokens
        force_reprocess: Whether to reprocess content even if previously processed
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if not urls:
        print("Error: No URLs provided to process.")
        return 1
    
    print(f"Starting ingestion pipeline for {len(urls)} URLs...")
    print(f"Chunk size: {chunk_size}, Overlap: {overlap}, Force reprocess: {force_reprocess}")
    
    # Create and run the ingestion pipeline
    pipeline = IngestionPipeline()
    result = pipeline.run_pipeline(
        urls=urls,
        chunk_size=chunk_size,
        overlap=overlap,
        force_reprocess=force_reprocess
    )
    
    if result["success"]:
        print(f"Pipeline completed successfully: {result['message']}")
        print(f"Results: {result['data']}")
        return 0
    else:
        print(f"Pipeline failed: {result['error']}")
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="URL Ingestion & Embedding Pipeline")
    parser.add_argument("urls", nargs="+", help="URLs to process")
    parser.add_argument("--chunk-size", type=int, default=800, 
                       help="Target size for text chunks in tokens (default: 800)")
    parser.add_argument("--overlap", type=int, default=100, 
                       help="Overlap between chunks in tokens (default: 100)")
    parser.add_argument("--force-reprocess", action="store_true", 
                       help="Re-process content even if previously processed")
    
    args = parser.parse_args()
    
    exit_code = main(
        urls=args.urls,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        force_reprocess=args.force_reprocess
    )
    
    sys.exit(exit_code)