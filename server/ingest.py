import os
import re
from pathlib import Path
from typing import List
import hashlib

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

if qdrant_api_key and qdrant_url:
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
elif qdrant_url:
    qdrant_client = QdrantClient(url=qdrant_url)
else:
    raise Exception("Qdrant URL not found in environment variables")

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split text into chunks of approximately chunk_size characters.
    Tries to break at sentence boundaries when possible.
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If we're not at the end, try to find a sentence boundary
        if end < len(text):
            # Look for sentence endings (., !, ?) near the end
            snippet = text[start:end]
            last_sentence_end = max(
                snippet.rfind('.'),
                snippet.rfind('!'),
                snippet.rfind('?')
            )
            
            # If we found a sentence boundary, use it
            if last_sentence_end != -1 and last_sentence_end > len(snippet) * 0.7:  # At least 70% through the chunk
                end = start + last_sentence_end + 1
            else:
                # Otherwise, look for a word boundary
                last_space = snippet.rfind(' ')
                if last_space != -1 and last_space > len(snippet) * 0.8:  # At least 80% through the chunk
                    end = start + last_space
        
        chunk = text[start:end].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
        
        start = end
    
    return chunks

def embed_text(text: str) -> List[float]:
    """
    Uses OpenAI text-embedding-3-small to convert text to vectors.
    """
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error embedding text: {e}")
        raise e

def ingest_file(file_path: Path, collection_name: str = "textbook_knowledge"):
    """
    Process a single markdown file and ingest its content into Qdrant.
    """
    print(f"Processing {file_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from the file (first heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem
    
    # Remove markdown headers and metadata from content
    # This regex removes YAML frontmatter if present
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Split content into chunks
    chunks = chunk_text(content)
    
    points = []
    for i, chunk in enumerate(chunks):
        # Create a unique ID for this chunk
        chunk_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
        
        # Embed the chunk
        try:
            vector = embed_text(chunk)
        except Exception as e:
            print(f"❌ Failed to embed chunk from {file_path}: {e}")
            continue
        
        # Create a Qdrant point
        point = models.PointStruct(
            id=chunk_id,
            vector=vector,
            payload={
                "content": chunk,
                "source": str(file_path.relative_to("../web/docs")),
                "title": title,
                "file_path": str(file_path)
            }
        )
        points.append(point)
    
    # Upload to Qdrant
    if points:
        try:
            # Create collection if it doesn't exist
            try:
                qdrant_client.get_collection(collection_name)
            except:
                # Collection doesn't exist, create it
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)  # OpenAI embedding size
                )
            
            # Upload points
            qdrant_client.upsert(
                collection_name=collection_name,
                points=points
            )
            
            print(f"✅ Ingested {file_path} ({len(points)} chunks)")
        except Exception as e:
            print(f"❌ Failed to upload {file_path} to Qdrant: {e}")
    else:
        print(f"⚠️ No content to upload for {file_path}")

def main():
    """
    Main function to scan the docs directory and ingest all markdown files.
    """
    docs_path = Path("../web/docs")
    
    if not docs_path.exists():
        print(f"❌ Docs directory {docs_path} does not exist")
        return
    
    # Find all markdown files in the docs directory
    md_files = list(docs_path.rglob("*.md"))
    
    if not md_files:
        print("No markdown files found in the docs directory")
        return
    
    print(f"Found {len(md_files)} markdown files to process")
    
    for file_path in md_files:
        try:
            ingest_file(file_path)
        except Exception as e:
            print(f"❌ Error processing file {file_path}: {e}")
    
    print("Ingestion complete!")

if __name__ == "__main__":
    main()