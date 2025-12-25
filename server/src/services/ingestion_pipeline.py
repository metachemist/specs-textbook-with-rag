from typing import Dict, Any, List
from src.services.base_service import BaseService
from src.services.url_fetch_service import URLFetchService
from src.services.text_cleaning_service import TextCleaningService
from src.services.chunking_service import ChunkingService
from src.services.embedding_service import EmbeddingService
from src.services.storage_service import StorageService
from src.models.url_content import URLContent
from src.models.clean_text import CleanText
from src.models.text_chunk import TextChunk
from src.models.embedding import Embedding
from src.models.metadata import Metadata
from src.models.ingestion_job import IngestionJob
from src.utils.helpers import generate_uuid, get_current_timestamp
from src.config.settings import settings


class IngestionPipeline(BaseService):
    """
    Orchestrates the full ingestion pipeline: fetch → clean → chunk → embed → store
    """
    
    def __init__(self):
        super().__init__("IngestionPipeline")
        self.url_fetch_service = URLFetchService()
        self.text_cleaning_service = TextCleaningService()
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.storage_service = StorageService()
    
    def run_pipeline(self, urls: List[str], 
                     chunk_size: int = None, 
                     overlap: int = None, 
                     force_reprocess: bool = False) -> Dict[str, Any]:
        """
        Execute the full ingestion pipeline from fetching to storage
        
        Args:
            urls: List of URLs to process
            chunk_size: Target size for text chunks (defaults to settings)
            overlap: Overlap between chunks (defaults to settings)
            force_reprocess: Whether to reprocess content even if previously processed
            
        Returns:
            Dictionary with success status and result or error
        """
        try:
            # Create ingestion job
            job_id = generate_uuid()
            ingestion_job = IngestionJob(
                id=job_id,
                status="pending",
                urls_to_process=urls,
                total_urls=len(urls),
                processed_urls=0,
                successful_chunks=0,
                failed_chunks=0,
                start_time=get_current_timestamp()
            )
            
            self.logger.info(f"Starting ingestion job {job_id} for {len(urls)} URLs")
            
            # Update job status
            ingestion_job.status = "fetching"
            
            # Process each URL
            all_embeddings = []
            all_metadata = []
            
            for i, url in enumerate(urls):
                self.logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")
                
                try:
                    # 1. Fetch content
                    self.logger.info(f"Fetching content from {url}")
                    fetch_result = self.url_fetch_service.fetch_content_with_retry(url)
                    
                    if not fetch_result["success"]:
                        self.logger.error(f"Failed to fetch {url}: {fetch_result['error']}")
                        ingestion_job.error_log.append({
                            "url": url,
                            "stage": "fetch",
                            "error": fetch_result["error"]
                        })
                        continue
                    
                    url_content: URLContent = fetch_result["data"]
                    ingestion_job.processed_urls += 1
                    
                    # 2. Clean content
                    self.logger.info(f"Cleaning content from {url}")
                    clean_result = self.text_cleaning_service.clean_content_with_encoding_handling(url_content)
                    
                    if not clean_result["success"]:
                        self.logger.error(f"Failed to clean content from {url}: {clean_result['error']}")
                        ingestion_job.error_log.append({
                            "url": url,
                            "stage": "clean",
                            "error": clean_result["error"]
                        })
                        continue
                    
                    clean_text: CleanText = clean_result["data"]
                    
                    # 3. Chunk content
                    self.logger.info(f"Chunking content from {url}")
                    chunk_result = self.chunking_service.chunk_text(clean_text)
                    
                    if not chunk_result["success"]:
                        self.logger.error(f"Failed to chunk content from {url}: {chunk_result['error']}")
                        ingestion_job.error_log.append({
                            "url": url,
                            "stage": "chunk",
                            "error": chunk_result["error"]
                        })
                        continue
                    
                    text_chunks: List[TextChunk] = chunk_result["data"]
                    
                    # 4. Generate embeddings
                    self.logger.info(f"Generating embeddings for {len(text_chunks)} chunks from {url}")
                    embedding_result = self.embedding_service.batch_generate_embeddings(text_chunks)
                    
                    if not embedding_result["success"]:
                        self.logger.error(f"Failed to generate embeddings for {url}: {embedding_result['error']}")
                        ingestion_job.error_log.append({
                            "url": url,
                            "stage": "embed",
                            "error": embedding_result["error"]
                        })
                        continue
                    
                    embeddings: List[Embedding] = embedding_result["data"]
                    
                    # 5. Create metadata for each chunk
                    metadata_list = []
                    for chunk in text_chunks:
                        metadata = Metadata(
                            url=chunk.url,
                            title=clean_text.original_url.split('/')[-1],  # Use filename as title for now
                            source_domain=clean_text.original_url.split('/')[2],  # Extract domain
                            chunk_index=chunk.chunk_index,
                            content_type="web_content",
                            created_at=chunk.created_at,
                            tags=["ingested", "web_content"]
                        )
                        metadata_list.append(metadata)
                    
                    # 6. Store embeddings
                    self.logger.info(f"Storing {len(embeddings)} embeddings for {url}")
                    store_result = self.storage_service.store_embeddings(embeddings, metadata_list)
                    
                    if not store_result["success"]:
                        self.logger.error(f"Failed to store embeddings for {url}: {store_result['error']}")
                        ingestion_job.error_log.append({
                            "url": url,
                            "stage": "store",
                            "error": store_result["error"]
                        })
                        continue
                    
                    # Update successful chunks count
                    ingestion_job.successful_chunks += len(embeddings)
                    
                    # Add to all results
                    all_embeddings.extend(embeddings)
                    all_metadata.extend(metadata_list)
                    
                    self.logger.info(f"Successfully processed {url}")
                    
                except Exception as e:
                    self.logger.error(f"Unexpected error processing {url}: {str(e)}")
                    ingestion_job.error_log.append({
                        "url": url,
                        "stage": "unknown",
                        "error": str(e)
                    })
                    continue
            
            # Update job status
            ingestion_job.status = "completed" if len(ingestion_job.error_log) == 0 else "partial_success"
            ingestion_job.end_time = get_current_timestamp()
            
            self.logger.info(f"Ingestion job {job_id} completed. "
                           f"Processed: {ingestion_job.processed_urls}/{ingestion_job.total_urls}, "
                           f"Successful chunks: {ingestion_job.successful_chunks}, "
                           f"Failed chunks: {ingestion_job.failed_chunks}")
            
            return self.handle_success(
                data={
                    "job_id": job_id,
                    "processed_urls": ingestion_job.processed_urls,
                    "successful_chunks": ingestion_job.successful_chunks,
                    "failed_chunks": len(ingestion_job.error_log),
                    "total_chunks": ingestion_job.successful_chunks + len(ingestion_job.error_log)
                },
                message=f"Ingestion pipeline completed. Processed {ingestion_job.processed_urls} URLs with {ingestion_job.successful_chunks} successful chunks."
            )
            
        except Exception as e:
            return self.handle_error(e, "run_pipeline")
    
    def run_pipeline_with_progress_tracking(self, urls: List[str], 
                                          chunk_size: int = None, 
                                          overlap: int = None, 
                                          force_reprocess: bool = False) -> Dict[str, Any]:
        """
        Execute the full ingestion pipeline with progress tracking
        
        Args:
            urls: List of URLs to process
            chunk_size: Target size for text chunks (defaults to settings)
            overlap: Overlap between chunks (defaults to settings)
            force_reprocess: Whether to reprocess content even if previously processed
            
        Returns:
            Dictionary with success status and result or error
        """
        try:
            # For now, just call the regular run_pipeline method
            # In the future, we could add more detailed progress tracking
            return self.run_pipeline(urls, chunk_size, overlap, force_reprocess)
        except Exception as e:
            return self.handle_error(e, "run_pipeline_with_progress_tracking")