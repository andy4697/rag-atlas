"""SQLAlchemy database models."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    Index,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.papers import PaperStatus
from src.models.resumes import ResumeStatus, ExperienceLevel

Base = declarative_base()


class TimestampMixin:
    """Mixin for timestamp fields."""
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Author(Base, TimestampMixin):
    """Author table."""
    
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    affiliation = Column(String(500))
    email = Column(String(255))
    orcid = Column(String(19))  # ORCID format: 0000-0000-0000-0000
    
    # Relationships
    paper_authors = relationship("PaperAuthor", back_populates="author")
    
    __table_args__ = (
        Index("idx_author_name", "name"),
        Index("idx_author_orcid", "orcid"),
    )


class Paper(Base, TimestampMixin):
    """Paper table."""
    
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String(20), unique=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    abstract = Column(Text, nullable=False)
    published_date = Column(DateTime(timezone=True), nullable=False, index=True)
    updated_date = Column(DateTime(timezone=True))
    
    # Content fields
    pdf_url = Column(String(500))
    pdf_path = Column(String(500))
    full_text = Column(Text)
    
    # Processing status
    status = Column(Enum(PaperStatus), default=PaperStatus.PENDING, nullable=False, index=True)
    processing_metadata = Column(JSON, default=dict)
    
    # Metrics
    citation_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    
    # Relationships
    paper_authors = relationship("PaperAuthor", back_populates="paper", cascade="all, delete-orphan")
    paper_categories = relationship("PaperCategory", back_populates="paper", cascade="all, delete-orphan")
    chunks = relationship("Chunk", back_populates="paper", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_paper_status", "status"),
        Index("idx_paper_published_date", "published_date"),
        Index("idx_paper_arxiv_id", "arxiv_id"),
    )


class PaperAuthor(Base):
    """Many-to-many relationship between papers and authors."""
    
    __tablename__ = "paper_authors"
    
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    author_order = Column(Integer, nullable=False)  # Order of authorship
    
    # Relationships
    paper = relationship("Paper", back_populates="paper_authors")
    author = relationship("Author", back_populates="paper_authors")
    
    __table_args__ = (
        UniqueConstraint("paper_id", "author_id", name="uq_paper_author"),
        Index("idx_paper_author_paper_id", "paper_id"),
        Index("idx_paper_author_author_id", "author_id"),
    )


class Category(Base, TimestampMixin):
    """arXiv categories table."""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)  # e.g., cs.AI, cs.CL
    name = Column(String(200), nullable=False)
    description = Column(Text)
    parent_category = Column(String(10))  # e.g., cs, math, physics
    
    # Relationships
    paper_categories = relationship("PaperCategory", back_populates="category")
    
    __table_args__ = (
        Index("idx_category_code", "code"),
        Index("idx_category_parent", "parent_category"),
    )


class PaperCategory(Base):
    """Many-to-many relationship between papers and categories."""
    
    __tablename__ = "paper_categories"
    
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    is_primary = Column(Boolean, default=False)  # Primary category for the paper
    
    # Relationships
    paper = relationship("Paper", back_populates="paper_categories")
    category = relationship("Category", back_populates="paper_categories")
    
    __table_args__ = (
        UniqueConstraint("paper_id", "category_id", name="uq_paper_category"),
        Index("idx_paper_category_paper_id", "paper_id"),
        Index("idx_paper_category_category_id", "category_id"),
    )


class Chunk(Base, TimestampMixin):
    """Text chunks from processed papers."""
    
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    
    # Semantic information
    section_title = Column(String(200))
    section_type = Column(String(50), index=True)  # abstract, introduction, methods, etc.
    
    # Vector embeddings (stored as JSON array)
    embedding = Column(JSON)  # List of floats
    embedding_model = Column(String(100))
    
    # Chunk metadata
    token_count = Column(Integer, default=0)
    char_count = Column(Integer, default=0)
    
    # Relationships
    paper = relationship("Paper", back_populates="chunks")
    
    __table_args__ = (
        Index("idx_chunk_paper_id", "paper_id"),
        Index("idx_chunk_section_type", "section_type"),
        Index("idx_chunk_paper_index", "paper_id", "chunk_index"),
    )


class Resume(Base, TimestampMixin):
    """Resume table."""
    
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500))
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, txt
    
    # Content
    original_text = Column(Text)
    parsed_data = Column(JSON)  # ParsedResumeData as JSON
    
    # Analysis results
    analysis_results = Column(JSON)  # AnalysisResult as JSON
    enhancement_suggestions = Column(JSON)  # List of Enhancement as JSON
    
    # Processing status
    status = Column(Enum(ResumeStatus), default=ResumeStatus.PENDING, nullable=False, index=True)
    processing_metadata = Column(JSON, default=dict)
    
    # Relationships
    job_matches = relationship("JobMatch", back_populates="resume", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_resume_user_id", "user_id"),
        Index("idx_resume_status", "status"),
        Index("idx_resume_created_at", "created_at"),
    )


class JobDescription(Base, TimestampMixin):
    """Job description table."""
    
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False, index=True)
    location = Column(String(100))
    employment_type = Column(String(50))  # full-time, part-time, contract
    experience_level = Column(Enum(ExperienceLevel), index=True)
    
    # Content
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=list)  # List of strings
    preferred_qualifications = Column(JSON, default=list)  # List of strings
    responsibilities = Column(JSON, default=list)  # List of strings
    
    # Extracted data
    required_skills = Column(JSON, default=list)  # List of strings
    preferred_skills = Column(JSON, default=list)  # List of strings
    keywords = Column(JSON, default=list)  # List of strings
    
    # Metadata
    salary_range = Column(String(100))
    benefits = Column(JSON, default=list)  # List of strings
    
    # Relationships
    job_matches = relationship("JobMatch", back_populates="job_description", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_job_title", "title"),
        Index("idx_job_company", "company"),
        Index("idx_job_experience_level", "experience_level"),
        Index("idx_job_created_at", "created_at"),
    )


class JobMatch(Base, TimestampMixin):
    """Job matching results table."""
    
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    
    # Matching scores
    overall_match_score = Column(Float, nullable=False)
    skill_match_score = Column(Float, nullable=False)
    experience_match_score = Column(Float, nullable=False)
    
    # Detailed analysis
    matching_skills = Column(JSON, default=list)  # List of strings
    missing_skills = Column(JSON, default=list)  # List of strings
    skill_gaps = Column(JSON, default=list)  # List of strings
    recommendations = Column(JSON, default=list)  # List of strings
    
    # Relationships
    job_description = relationship("JobDescription", back_populates="job_matches")
    resume = relationship("Resume", back_populates="job_matches")
    
    __table_args__ = (
        UniqueConstraint("job_id", "resume_id", name="uq_job_resume_match"),
        Index("idx_job_match_job_id", "job_id"),
        Index("idx_job_match_resume_id", "resume_id"),
        Index("idx_job_match_overall_score", "overall_match_score"),
    )