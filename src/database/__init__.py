"""Database package initialization."""

from .connection import get_db, engine, SessionLocal, async_engine, AsyncSessionLocal
from .models import (
    Base,
    Author,
    Paper,
    PaperAuthor,
    Category,
    PaperCategory,
    Chunk,
    Resume,
    JobDescription,
    JobMatch,
)
from .repositories import (
    BaseRepository,
    PaperRepository,
    AuthorRepository,
    ChunkRepository,
    ResumeRepository,
    JobDescriptionRepository,
    JobMatchRepository,
)
from .repositories.factory import RepositoryFactory, get_repositories

__all__ = [
    "get_db",
    "engine", 
    "SessionLocal",
    "async_engine",
    "AsyncSessionLocal",
    "Base",
    "Author",
    "Paper", 
    "PaperAuthor",
    "Category",
    "PaperCategory",
    "Chunk",
    "Resume",
    "JobDescription",
    "JobMatch",
    "BaseRepository",
    "PaperRepository",
    "AuthorRepository",
    "ChunkRepository",
    "ResumeRepository",
    "JobDescriptionRepository",
    "JobMatchRepository",
    "RepositoryFactory",
    "get_repositories",
]