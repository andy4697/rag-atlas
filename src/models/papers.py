"""Data models for research papers and related entities."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, validator
from .base import TimestampMixin


class PaperStatus(str, Enum):
    """Status of paper processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Author(BaseModel):
    """Author information model."""
    name: str = Field(..., min_length=1, max_length=200)
    affiliation: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    orcid: Optional[str] = Field(None, regex=r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$')
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "affiliation": "MIT Computer Science",
                "email": "john.doe@mit.edu",
                "orcid": "0000-0000-0000-0000"
            }
        }


class PaperMetadata(BaseModel):
    """Paper metadata from arXiv or other sources."""
    arxiv_id: Optional[str] = Field(None, regex=r'^\d{4}\.\d{4,5}(v\d+)?$')
    doi: Optional[str] = Field(None, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=10, max_length=5000)
    authors: List[Author] = Field(..., min_items=1)
    categories: List[str] = Field(default_factory=list, max_items=10)
    keywords: List[str] = Field(default_factory=list, max_items=20)
    published_date: datetime
    updated_date: Optional[datetime] = None
    journal: Optional[str] = Field(None, max_length=200)
    volume: Optional[str] = Field(None, max_length=50)
    pages: Optional[str] = Field(None, max_length=50)
    
    @validator('categories', 'keywords')
    def validate_string_lists(cls, v):
        """Ensure all items in lists are non-empty strings."""
        return [item.strip() for item in v if item and item.strip()]


class Paper(TimestampMixin):
    """Complete paper model with content and metadata."""
    id: Optional[int] = None
    arxiv_id: Optional[str] = Field(None, regex=r'^\d{4}\.\d{4,5}(v\d+)?$')
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=10, max_length=5000)
    authors: List[Author] = Field(..., min_items=1)
    categories: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    published_date: datetime
    updated_date: Optional[datetime] = None
    
    # Content fields
    pdf_url: Optional[HttpUrl] = None
    pdf_path: Optional[str] = Field(None, max_length=500)
    full_text: Optional[str] = None
    
    # Processing status
    status: PaperStatus = PaperStatus.PENDING
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Metrics
    citation_count: int = Field(default=0, ge=0)
    download_count: int = Field(default=0, ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "arxiv_id": "2301.00001",
                "title": "Attention Is All You Need",
                "abstract": "The dominant sequence transduction models...",
                "authors": [
                    {
                        "name": "Ashish Vaswani",
                        "affiliation": "Google Brain"
                    }
                ],
                "categories": ["cs.CL", "cs.AI"],
                "keywords": ["transformer", "attention", "neural networks"],
                "published_date": "2023-01-01T00:00:00Z",
                "status": "completed"
            }
        }


class Chunk(TimestampMixin):
    """Text chunk from processed papers."""
    id: Optional[int] = None
    paper_id: int = Field(..., description="Foreign key to paper")
    content: str = Field(..., min_length=10, max_length=10000)
    chunk_index: int = Field(..., ge=0, description="Order within the paper")
    
    # Semantic information
    section_title: Optional[str] = Field(None, max_length=200)
    section_type: Optional[str] = Field(None, max_length=50)  # abstract, introduction, methods, etc.
    
    # Vector embeddings (stored as JSON in DB)
    embedding: Optional[List[float]] = Field(None, description="Vector embedding")
    embedding_model: Optional[str] = Field(None, max_length=100)
    
    # Chunk metadata
    token_count: int = Field(default=0, ge=0)
    char_count: int = Field(default=0, ge=0)
    
    @validator('embedding')
    def validate_embedding_dimension(cls, v):
        """Validate embedding dimension if provided."""
        if v is not None and len(v) not in [384, 512, 768, 1024, 1536]:
            raise ValueError("Embedding dimension must be one of: 384, 512, 768, 1024, 1536")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "paper_id": 1,
                "content": "The Transformer model architecture is based entirely on attention mechanisms...",
                "chunk_index": 0,
                "section_title": "Introduction",
                "section_type": "introduction",
                "token_count": 150,
                "char_count": 800
            }
        }


# API Request/Response Models
class PaperSearchRequest(BaseModel):
    """Request model for paper search."""
    query: str = Field(..., min_length=1, max_length=500)
    categories: Optional[List[str]] = Field(None, max_items=5)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    max_results: int = Field(default=10, ge=1, le=100)
    include_abstract: bool = Field(default=True)
    
    class Config:
        schema_extra = {
            "example": {
                "query": "transformer neural networks",
                "categories": ["cs.CL", "cs.AI"],
                "max_results": 20,
                "include_abstract": True
            }
        }


class PaperSearchResponse(BaseModel):
    """Response model for paper search."""
    papers: List[Paper]
    total_count: int = Field(..., ge=0)
    query: str
    search_time_ms: float = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "papers": [],
                "total_count": 42,
                "query": "transformer neural networks",
                "search_time_ms": 150.5
            }
        }


class PaperIngestRequest(BaseModel):
    """Request model for paper ingestion."""
    arxiv_id: Optional[str] = Field(None, regex=r'^\d{4}\.\d{4,5}(v\d+)?$')
    pdf_url: Optional[HttpUrl] = None
    force_reprocess: bool = Field(default=False)
    
    @validator('arxiv_id', 'pdf_url')
    def validate_source(cls, v, values):
        """Ensure at least one source is provided."""
        if not v and not values.get('pdf_url'):
            raise ValueError("Either arxiv_id or pdf_url must be provided")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "arxiv_id": "2301.00001",
                "force_reprocess": False
            }
        }


class ChunkSearchRequest(BaseModel):
    """Request model for semantic chunk search."""
    query: str = Field(..., min_length=1, max_length=500)
    paper_ids: Optional[List[int]] = Field(None, max_items=50)
    section_types: Optional[List[str]] = Field(None, max_items=10)
    max_results: int = Field(default=10, ge=1, le=100)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "query": "attention mechanism implementation",
                "section_types": ["methods", "results"],
                "max_results": 15,
                "similarity_threshold": 0.75
            }
        }


class ChunkSearchResult(BaseModel):
    """Individual chunk search result with metadata."""
    chunk: Chunk
    paper: Paper
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    rank: int = Field(..., ge=1)
    
    class Config:
        schema_extra = {
            "example": {
                "chunk": {},
                "paper": {},
                "similarity_score": 0.85,
                "rank": 1
            }
        }


class ChunkSearchResponse(BaseModel):
    """Response model for chunk search."""
    results: List[ChunkSearchResult]
    total_count: int = Field(..., ge=0)
    query: str
    search_time_ms: float = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "results": [],
                "total_count": 25,
                "query": "attention mechanism implementation",
                "search_time_ms": 89.3
            }
        }