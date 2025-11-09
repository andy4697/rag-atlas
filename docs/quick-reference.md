# Quick Reference - Database Operations

## Getting Started (Copy-Paste Ready)

### Basic Setup
```python
from src.database import get_db, get_repositories

async def your_function():
    async with get_db() as session:
        repos = get_repositories(session)
        # Use repos here...
```

## Paper Operations

### Add a Paper
```python
paper = await repos.papers.create(
    title="Your Paper Title",
    abstract="Paper abstract text...",
    published_date=datetime.now(),
    arxiv_id="2024.12345"  # Optional
)
```

### Search Papers
```python
# By title
papers = await repos.papers.search_by_title("machine learning")

# By abstract content
papers = await repos.papers.search_by_abstract("neural networks")

# Recent papers (last 7 days)
recent = await repos.papers.get_recent_papers(days=7)

# By date range
papers = await repos.papers.get_by_date_range(start_date, end_date)

# By status
pending = await repos.papers.get_by_status("pending")
```

### Get Paper Details
```python
# Basic paper info
paper = await repos.papers.get_by_id(123)

# Paper with authors
paper_with_authors = await repos.papers.get_with_authors(123)

# Paper with text chunks
paper_with_chunks = await repos.papers.get_with_chunks(123)
```

### Update Paper
```python
# Update status
updated = await repos.papers.update_processing_status(
    paper_id=123,
    status="completed",
    metadata={"processing_time": 45.2}
)

# General update
updated = await repos.papers.update(123, title="New Title")
```

## Author Operations

### Add Author
```python
author = await repos.authors.create(
    name="Dr. Jane Smith",
    affiliation="MIT",
    email="jane@mit.edu",
    orcid="0000-0000-0000-0000"  # Optional
)
```

### Find Authors
```python
# By name
author = await repos.authors.get_by_name("Dr. Jane Smith")

# Search by partial name
authors = await repos.authors.search_by_name("Smith")

# Get author with their papers
author_with_papers = await repos.authors.get_with_papers(author_id)

# Get or create (useful for imports)
author = await repos.authors.get_or_create(
    name="Dr. John Doe",
    affiliation="Stanford"
)
```

## Text Chunk Operations

### Add Chunks (Usually done automatically)
```python
chunks_data = [
    {
        "paper_id": 123,
        "content": "This is the first chunk...",
        "chunk_index": 0,
        "section_type": "introduction"
    },
    {
        "paper_id": 123,
        "content": "This is the second chunk...",
        "chunk_index": 1,
        "section_type": "methods"
    }
]
chunks = await repos.chunks.bulk_create(chunks_data)
```

### Search Chunks
```python
# Get all chunks for a paper
chunks = await repos.chunks.get_by_paper_id(123)

# Search chunk content
chunks = await repos.chunks.search_content("neural networks")

# Get chunks by section type
intro_chunks = await repos.chunks.get_by_section_type("introduction")

# Get chunks with embeddings
embedded_chunks = await repos.chunks.get_chunks_with_embeddings()
```

### Update Chunk Embeddings
```python
# Single chunk
await repos.chunks.update_embedding(
    chunk_id=456,
    embedding=[0.1, 0.2, 0.3, ...],  # Vector of floats
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Multiple chunks
chunk_embeddings = [
    {
        "chunk_id": 456,
        "embedding": [0.1, 0.2, ...],
        "model": "all-MiniLM-L6-v2"
    },
    # ... more chunks
]
await repos.chunks.bulk_update_embeddings(chunk_embeddings)
```

## Resume Operations

### Upload Resume
```python
resume = await repos.resumes.create(
    user_id="user123",
    filename="john_doe_resume.pdf",
    file_size=245760,
    file_type="pdf",
    status="pending"
)
```

### Get User Resumes
```python
# All resumes for a user
user_resumes = await repos.resumes.get_by_user_id("user123")

# Resumes by status
pending = await repos.resumes.get_by_status("processing")

# Recent resumes
recent = await repos.resumes.get_recent_resumes(days=30)
```

### Update Resume Analysis
```python
# Update parsed data
await repos.resumes.update_parsed_data(
    resume_id=123,
    parsed_data={
        "full_name": "John Doe",
        "email": "john@email.com",
        "skills": ["Python", "Machine Learning"],
        "experience": [...]
    }
)

# Update analysis results
await repos.resumes.update_analysis_results(
    resume_id=123,
    analysis_results={
        "completeness_score": 0.85,
        "ats_compatibility_score": 0.78,
        "strengths": ["Strong technical skills"]
    },
    enhancement_suggestions=[
        {
            "section": "experience",
            "type": "modification",
            "description": "Add quantified achievements",
            "priority": "high"
        }
    ]
)
```

## Job Description Operations

### Add Job Description
```python
job = await repos.job_descriptions.create(
    title="Senior Software Engineer",
    company="Tech Corp",
    location="San Francisco, CA",
    employment_type="full-time",
    experience_level="senior",
    description="We are looking for...",
    required_skills=["Python", "React", "PostgreSQL"],
    salary_range="$120,000 - $160,000"
)
```

### Search Jobs
```python
# By title
jobs = await repos.job_descriptions.search_by_title("Software Engineer")

# By company
jobs = await repos.job_descriptions.search_by_company("Google")

# By experience level
senior_jobs = await repos.job_descriptions.get_by_experience_level("senior")

# By location
sf_jobs = await repos.job_descriptions.get_by_location("San Francisco")
```

## Job Matching Operations

### Create Job Match
```python
match = await repos.job_matches.create_or_update_match(
    job_id=456,
    resume_id=123,
    overall_match_score=0.85,
    skill_match_score=0.90,
    experience_match_score=0.80,
    matching_skills=["Python", "PostgreSQL"],
    missing_skills=["React"],
    recommendations=["Add React experience", "Highlight Python projects"]
)
```

### Find Matches
```python
# Top matches for a resume
top_matches = await repos.job_matches.get_top_matches(
    resume_id=123,
    min_score=0.7,
    limit=10
)

# All matches for a job
job_matches = await repos.job_matches.get_by_job_id(456)

# Specific match
match = await repos.job_matches.get_match(job_id=456, resume_id=123)

# Match with full details
detailed_match = await repos.job_matches.get_with_details(match_id=789)
```

## Common Patterns

### Error Handling
```python
try:
    paper = await repos.papers.get_by_id(123)
    if not paper:
        print("Paper not found")
except Exception as e:
    print(f"Database error: {e}")
```

### Pagination
```python
# Get first 20 papers
papers = await repos.papers.get_all(limit=20, offset=0)

# Get next 20 papers
papers = await repos.papers.get_all(limit=20, offset=20)
```

### Filtering
```python
# Multiple filters
papers = await repos.papers.get_by_filters({
    "status": "completed",
    "published_date": datetime(2024, 1, 1)
})
```

### Counting
```python
# Count all papers
total = await repos.papers.count()

# Count with filters
completed_count = await repos.papers.count({"status": "completed"})
```

### Check Existence
```python
# Check if paper exists
exists = await repos.papers.exists(arxiv_id="2024.12345")
```

## Complete Example: Paper Processing Pipeline

```python
async def process_paper_from_arxiv(arxiv_id: str):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # 1. Check if paper already exists
        existing = await repos.papers.get_by_arxiv_id(arxiv_id)
        if existing:
            return existing
        
        # 2. Create paper record
        paper = await repos.papers.create(
            arxiv_id=arxiv_id,
            title="Downloaded from arXiv",  # Will update later
            abstract="Processing...",
            published_date=datetime.now(),
            status="pending"
        )
        
        # 3. Update status to processing
        await repos.papers.update_processing_status(
            paper.id, 
            "processing"
        )
        
        # 4. After downloading and parsing...
        await repos.papers.update(
            paper.id,
            title="Actual Paper Title",
            abstract="Actual abstract text...",
            full_text="Full paper content..."
        )
        
        # 5. Create text chunks
        chunks_data = [
            {
                "paper_id": paper.id,
                "content": chunk_text,
                "chunk_index": i,
                "section_type": section_type
            }
            for i, (chunk_text, section_type) in enumerate(chunks)
        ]
        await repos.chunks.bulk_create(chunks_data)
        
        # 6. Mark as completed
        await repos.papers.update_processing_status(
            paper.id,
            "completed",
            {"chunks_created": len(chunks_data)}
        )
        
        return paper
```

This gives you everything you need to work with the database layer!