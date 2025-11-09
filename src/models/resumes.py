"""Data models for resumes and job descriptions."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
from .base import TimestampMixin


class ResumeStatus(str, Enum):
    """Status of resume processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EnhancementType(str, Enum):
    """Type of resume enhancement."""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    JOB_SPECIFIC = "job_specific"


class ExperienceLevel(str, Enum):
    """Experience level categories."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXECUTIVE = "executive"


class Contact(BaseModel):
    """Contact information model."""
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, max_length=20)
    linkedin: Optional[str] = Field(None, max_length=200)
    github: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, max_length=300)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@email.com",
                "phone": "+1-555-123-4567",
                "linkedin": "https://linkedin.com/in/johndoe",
                "github": "https://github.com/johndoe"
            }
        }


class Education(BaseModel):
    """Education entry model."""
    institution: str = Field(..., min_length=1, max_length=200)
    degree: str = Field(..., min_length=1, max_length=100)
    field_of_study: Optional[str] = Field(None, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    honors: Optional[List[str]] = Field(default_factory=list)
    relevant_coursework: Optional[List[str]] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "institution": "MIT",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2018-09-01T00:00:00Z",
                "end_date": "2022-05-01T00:00:00Z",
                "gpa": 3.8,
                "honors": ["Magna Cum Laude", "Dean's List"]
            }
        }


class Experience(BaseModel):
    """Work experience entry model."""
    company: str = Field(..., min_length=1, max_length=200)
    position: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: bool = Field(default=False)
    description: Optional[str] = Field(None, max_length=2000)
    achievements: Optional[List[str]] = Field(default_factory=list)
    technologies: Optional[List[str]] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "company": "Tech Corp",
                "position": "Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2022-06-01T00:00:00Z",
                "is_current": True,
                "description": "Developed scalable web applications...",
                "achievements": ["Improved system performance by 40%"],
                "technologies": ["Python", "React", "PostgreSQL"]
            }
        }


class Skill(BaseModel):
    """Skill entry model."""
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    proficiency: Optional[str] = Field(None, max_length=20)  # beginner, intermediate, advanced, expert
    years_experience: Optional[int] = Field(None, ge=0, le=50)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "category": "Programming Languages",
                "proficiency": "advanced",
                "years_experience": 5
            }
        }


class ParsedResumeData(BaseModel):
    """Structured data extracted from resume."""
    full_name: Optional[str] = Field(None, max_length=100)
    contact: Optional[Contact] = None
    summary: Optional[str] = Field(None, max_length=1000)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "contact": {},
                "summary": "Experienced software engineer with 5+ years...",
                "education": [],
                "experience": [],
                "skills": []
            }
        }


class AnalysisResult(BaseModel):
    """Resume analysis results."""
    completeness_score: float = Field(..., ge=0.0, le=1.0)
    ats_compatibility_score: float = Field(..., ge=0.0, le=1.0)
    keyword_density: Dict[str, float] = Field(default_factory=dict)
    missing_sections: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "completeness_score": 0.85,
                "ats_compatibility_score": 0.78,
                "keyword_density": {"python": 0.05, "machine learning": 0.03},
                "missing_sections": ["certifications"],
                "improvement_areas": ["Add quantified achievements"],
                "strengths": ["Strong technical skills", "Clear experience progression"]
            }
        }


class Enhancement(BaseModel):
    """Resume enhancement suggestion."""
    section: str = Field(..., max_length=50)
    type: str = Field(..., max_length=50)  # addition, modification, removal
    description: str = Field(..., max_length=500)
    priority: str = Field(..., max_length=20)  # high, medium, low
    original_text: Optional[str] = Field(None, max_length=1000)
    suggested_text: Optional[str] = Field(None, max_length=1000)
    
    class Config:
        schema_extra = {
            "example": {
                "section": "experience",
                "type": "modification",
                "description": "Add quantified achievement to highlight impact",
                "priority": "high",
                "original_text": "Improved system performance",
                "suggested_text": "Improved system performance by 40%, reducing response time from 2s to 1.2s"
            }
        }


class Resume(TimestampMixin):
    """Complete resume model."""
    id: Optional[int] = None
    user_id: Optional[str] = Field(None, max_length=100)
    filename: str = Field(..., max_length=255)
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: int = Field(..., ge=0)
    file_type: str = Field(..., max_length=20)  # pdf, docx, txt
    
    # Parsed content
    original_text: Optional[str] = None
    parsed_data: Optional[ParsedResumeData] = None
    
    # Analysis results
    analysis_results: Optional[AnalysisResult] = None
    enhancement_suggestions: List[Enhancement] = Field(default_factory=list)
    
    # Processing status
    status: ResumeStatus = ResumeStatus.PENDING
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "filename": "john_doe_resume.pdf",
                "file_size": 245760,
                "file_type": "pdf",
                "status": "completed"
            }
        }


class JobDescription(TimestampMixin):
    """Job description model."""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)  # full-time, part-time, contract
    experience_level: Optional[ExperienceLevel] = None
    
    # Content
    description: str = Field(..., min_length=10, max_length=10000)
    requirements: List[str] = Field(default_factory=list)
    preferred_qualifications: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    
    # Extracted data
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    
    # Metadata
    salary_range: Optional[str] = Field(None, max_length=100)
    benefits: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "employment_type": "full-time",
                "experience_level": "senior",
                "description": "We are looking for a senior software engineer...",
                "required_skills": ["Python", "React", "PostgreSQL"],
                "salary_range": "$120,000 - $160,000"
            }
        }


class JobMatch(BaseModel):
    """Job matching analysis result."""
    job_id: int
    resume_id: int
    overall_match_score: float = Field(..., ge=0.0, le=1.0)
    skill_match_score: float = Field(..., ge=0.0, le=1.0)
    experience_match_score: float = Field(..., ge=0.0, le=1.0)
    
    # Detailed analysis
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    skill_gaps: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "job_id": 1,
                "resume_id": 1,
                "overall_match_score": 0.82,
                "skill_match_score": 0.85,
                "experience_match_score": 0.78,
                "matching_skills": ["Python", "React"],
                "missing_skills": ["Kubernetes", "AWS"],
                "recommendations": ["Highlight cloud experience", "Add DevOps skills"]
            }
        }


# API Request/Response Models
class ResumeUploadRequest(BaseModel):
    """Request model for resume upload."""
    enhancement_type: EnhancementType = EnhancementType.COMPREHENSIVE
    target_job_id: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "enhancement_type": "comprehensive",
                "target_job_id": 1
            }
        }


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis."""
    resume: Resume
    analysis: AnalysisResult
    enhancements: List[Enhancement]
    processing_time_ms: float = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "resume": {},
                "analysis": {},
                "enhancements": [],
                "processing_time_ms": 1250.5
            }
        }


class JobMatchRequest(BaseModel):
    """Request model for job matching."""
    resume_id: int = Field(..., gt=0)
    job_description: str = Field(..., min_length=10, max_length=10000)
    
    class Config:
        schema_extra = {
            "example": {
                "resume_id": 1,
                "job_description": "We are looking for a senior software engineer with Python experience..."
            }
        }


class JobMatchResponse(BaseModel):
    """Response model for job matching."""
    match_result: JobMatch
    customization_suggestions: List[Enhancement]
    processing_time_ms: float = Field(..., ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "match_result": {},
                "customization_suggestions": [],
                "processing_time_ms": 890.3
            }
        }


class ResumeGenerationRequest(BaseModel):
    """Request model for resume generation."""
    resume_id: int = Field(..., gt=0)
    format: str = Field(..., regex=r'^(pdf|docx|html)$')
    template: Optional[str] = Field(None, max_length=50)
    include_enhancements: bool = Field(default=True)
    
    class Config:
        schema_extra = {
            "example": {
                "resume_id": 1,
                "format": "pdf",
                "template": "modern",
                "include_enhancements": True
            }
        }