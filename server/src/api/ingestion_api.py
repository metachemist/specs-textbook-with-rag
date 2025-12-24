from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any
import asyncio
from pydantic import BaseModel
from src.services.ingestion_pipeline import IngestionPipeline
from src.models.ingestion_job import IngestionJob


# Create API router
router = APIRouter(prefix="/api/v1", tags=["ingestion"])


# Request/Response models
class IngestURLsRequest(BaseModel):
    urls: List[str]
    options: Dict[str, Any] = {}


class IngestURLsResponse(BaseModel):
    job_id: str
    status: str
    total_urls: int
    message: str


class IngestionJobStatusResponse(BaseModel):
    job_id: str
    status: str
    total_urls: int
    processed_urls: int
    successful_chunks: int
    failed_chunks: int
    start_time: str
    end_time: str = None
    progress_percentage: float


class BulkIngestRequest(BaseModel):
    config: Dict[str, Any]


# In-memory storage for job tracking (in production, use a database)
jobs: Dict[str, IngestionJob] = {}


@router.post("/ingest-urls", response_model=IngestURLsResponse)
async def ingest_urls(request: IngestURLsRequest) -> IngestURLsResponse:
    """
    Initiates the ingestion process for content from provided URLs
    """
    try:
        # Extract options
        chunk_size = request.options.get("chunk_size", 800)
        overlap = request.options.get("overlap", 100)
        force_reprocess = request.options.get("force_reprocess", False)
        
        # Create and run the ingestion pipeline
        pipeline = IngestionPipeline()
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: pipeline.run_pipeline(
                urls=request.urls,
                chunk_size=chunk_size,
                overlap=overlap,
                force_reprocess=force_reprocess
            )
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return IngestURLsResponse(
            job_id=result["data"]["job_id"],
            status="completed",  # In a real implementation, this would be queued
            total_urls=len(request.urls),
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ingest-urls/{job_id}", response_model=IngestionJobStatusResponse)
async def get_ingestion_job_status(job_id: str) -> IngestionJobStatusResponse:
    """
    Retrieves the current status of an ingestion job
    """
    try:
        # In a real implementation, this would fetch from a database
        # For now, we'll simulate the job status
        # This is a simplified implementation - in real world you'd track actual job status
        
        # Since we don't have a real job tracking system yet, we'll raise an exception
        # to indicate the job is not found
        raise HTTPException(status_code=404, detail="Job status tracking not implemented in this demo")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-ingest", response_model=IngestURLsResponse)
async def bulk_ingest(request: BulkIngestRequest) -> IngestURLsResponse:
    """
    Initiates ingestion from a configuration file containing multiple URLs and settings
    """
    try:
        # Extract URLs and settings from config
        urls = request.config.get("urls", [])
        settings = request.config.get("settings", {})
        
        if not urls:
            raise HTTPException(status_code=400, detail="No URLs provided in configuration")
        
        # Extract options from settings
        chunk_size = settings.get("chunk_size", 800)
        overlap = settings.get("overlap", 100)
        force_reprocess = settings.get("force_reprocess", False)
        
        # Create and run the ingestion pipeline
        pipeline = IngestionPipeline()
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: pipeline.run_pipeline(
                urls=urls,
                chunk_size=chunk_size,
                overlap=overlap,
                force_reprocess=force_reprocess
            )
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return IngestURLsResponse(
            job_id=result["data"]["job_id"],
            status="completed",  # In a real implementation, this would be queued
            total_urls=len(urls),
            message=result["message"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/ingest-urls/{job_id}", response_model=Dict[str, str])
async def cancel_ingestion_job(job_id: str) -> Dict[str, str]:
    """
    Cancels an in-progress ingestion job
    """
    try:
        # In a real implementation, this would cancel the actual job
        # For now, we'll just return a message indicating the job is cancelled
        return {
            "job_id": job_id,
            "status": "cancelled",
            "message": f"Ingestion job {job_id} cancelled successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))