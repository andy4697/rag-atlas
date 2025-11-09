# Task 2: Database Models Quick Reference

## Quick Start

```python
from src.database import get_db, get_repositories

async def your_function():
    async with get_db() as session:
        repos = get_repositories(session)
        # Use repos here...
```

## Pydantic Models (Data Validation)

### Paper Models

```python
from src.models.papers import Paper, Author, Chunk, PaperSearchRequest

# Create paper object
paper = Paper(
    title="Research Paper Title",
    abstract="This paper discusses...",
    authors=[
        Author(name="Dr. Smith", affiliation="MIT")
    ],
    published_date=datetime.now(),
    status="pending"
)

# Validate automatically
paper.title = ""  # ValidationError: title too short
```

### Resume Models

```python
from src.models.resumes import Resume, JobDescription, JobMatch

# Create resume object
resume = Resume(
    user_id="user123",
    filename="resume.pdf",
    file_size=245760,
    file_type="pdf"
)

# Job description
job = JobDescription(
    title="Software Engineer",
    company="Tech Corp",
    description="We are looking for...",
    required_skills=["Python", "React"]
)
```

## Database Operations (Repositories)

### Paper Operations

```python
# Create paper
paper = await repos.papers.create(
    title="My Research Paper",
    abstract="Abstract text...",
    published_date=datetime.now()
)

# Search papers
papers = await repos.papers.search_by_title("machine learning")
papers = await repos.papers.search_by_abstract("neural networks")
recent = await repos.papers.get_recent_papers(days=7)

# Get paper details
paper = await repos.papers.get_by_id(123)
paper_with_authors = await repos.papers.get_with_authors(123)
paper_with_chunks = await repos.papers.get_with_chunks(123)

# Update paper
await repos.papers.update(123, title="New Title")
await repos.papers.update_processing_status(123, "completed")

# Delete paper
await repos.papers.delete(123)
```

### Author Operations

```python
# Create author
author = await repos.authors.create(
    name="Dr. Jane Smith",
    affiliation="MIT",
    email="jane@mit.edu"
)

# Find author
author = await repos.authors.get_by_name("Dr. Jane Smith")
authors = await repos.authors.search_by_name("Smith")

# Get or create (useful for imports)
author = await repos.authors.get_or_create(
    name="Dr. John Doe",
    affiliation="Stanford"
)
```

### Chunk Operations

```python
# Create chunks (usually bulk)
chunks_data = [
    {
        "paper_id": 123,
        "content": "First chunk text...",
        "chunk_index": 0,
        "section_type": "introduction"
    },
    {
        "paper_id": 123,
        "content": "Second chunk text...",
        "chunk_index": 1,
        "section_type": "methods"
    }
]
chunks = await repos.chunks.bulk_create(chunks_data)

# Get chunks for paper
chunks = await repos.chunks.get_by_paper_id(123)

# Search chunk content
chunks = await repos.chunks.search_content("neural networks")

# Update embeddings
await repos.chunks.update_embedding(
    chunk_id=456,
    embedding=[0.1, 0.2, 0.3, ...],
    model="all-MiniLM-L6-v2"
)
```

### Resume Operations

```python
# Create resume
resume = await repos.resumes.create(
    user_id="user123",
    filename="resume.pdf",
    file_size=245760,
    file_type="pdf"
)

# Get user resumes
resumes = await repos.resumes.get_by_user_id("user123")

# Update parsed data
await repos.resumes.update_parsed_data(
    resume_id=123,
    parsed_data={
        "full_name": "John Doe",
        "email": "john@email.com",
        "skills": ["Python", "React"]
    }
)

# Update analysis
await repos.resumes.update_analysis_results(
    resume_id=123,
    analysis_results={
        "completeness_score": 0.85,
        "ats_compatibility_score": 0.78
    },
    enhancement_suggestions=[...]
)
```

### Job Description Operations

```python
# Create job
job = await repos.job_descriptions.create(
    title="Senior Software Engineer",
    company="Tech Corp",
    location="San Francisco, CA",
    description="We are looking for...",
    required_skills=["Python", "React", "PostgreSQL"]
)

# Search jobs
jobs = await repos.job_descriptions.search_by_title("Engineer")
jobs = await repos.job_descriptions.search_by_company("Google")
jobs = await repos.job_descriptions.get_by_experience_level("senior")
```

### Job Matching Operations

```python
# Create or update match
match = await repos.job_matches.create_or_update_match(
    job_id=456,
    resume_id=123,
    overall_match_score=0.85,
    skill_match_score=0.90,
    experience_match_score=0.80,
    matching_skills=["Python", "PostgreSQL"],
    missing_skills=["React"]
)

# Get top matches
matches = await repos.job_matches.get_top_matches(
    resume_id=123,
    min_score=0.7
)

# Get match details
match = await repos.job_matches.get_with_details(match_id=789)
```

## Common Patterns

### Pattern 1: Complete Paper Processing

```python
async def process_paper(arxiv_id: str):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # 1. Create paper
        paper = await repos.papers.create(
            arxiv_id=arxiv_id,
            title="Processing...",
            abstract="Downloading...",
            published_date=datetime.now(),
            status="pending"
        )
        
        # 2. Download and parse
        content = await download_paper(arxiv_id)
        metadata = await parse_metadata(content)
        
        # 3. Update paper
        await repos.papers.update(
            paper.id,
            title=metadata["title"],
            abstract=metadata["abstract"],
            full_text=content
        )
        
        # 4. Create chunks
        chunks = await create_chunks(content)
        chunks_data = [
            {
                "paper_id": paper.id,
                "content": chunk,
                "chunk_index": i,
                "section_type": get_section_type(chunk)
            }
            for i, chunk in enumerate(chunks)
        ]
        await repos.chunks.bulk_create(chunks_data)
        
        # 5. Mark complete
        await repos.papers.update_processing_status(
            paper.id,
            "completed",
            {"chunks_created": len(chunks)}
        )
        
        return paper
```

### Pattern 2: Resume Analysis Pipeline

```python
async def analyze_resume(user_id: str, file_path: str):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # 1. Create resume record
        resume = await repos.resumes.create(
            user_id=user_id,
            filename=os.path.basename(file_path),
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            file_type="pdf",
            status="processing"
        )
        
        # 2. Parse resume
        parsed_data = await parse_resume(file_path)
        await repos.resumes.update_parsed_data(
            resume.id,
            parsed_data
        )
        
        # 3. Analyze quality
        analysis = await analyze_resume_quality(parsed_data)
        suggestions = await generate_suggestions(parsed_data, analysis)
        
        await repos.resumes.update_analysis_results(
            resume.id,
            analysis,
            suggestions
        )
        
        # 4. Find job matches
        jobs = await repos.job_descriptions.get_all(limit=100)
        for job in jobs:
            score = await calculate_match_score(parsed_data, job)
            if score > 0.5:
                await repos.job_matches.create_or_update_match(
                    job.id,
                    resume.id,
                    overall_match_score=score,
                    skill_match_score=score,
                    experience_match_score=score
                )
        
        # 5. Mark complete
        await repos.resumes.update_processing_status(
            resume.id,
            "completed"
        )
        
        return resume
```

### Pattern 3: Search and Filter

```python
async def search_papers(query: str, filters: dict):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Search by title
        papers = await repos.papers.search_by_title(query)
        
        # Apply filters
        if filters.get("date_from"):
            papers = [p for p in papers if p.published_date >= filters["date_from"]]
        
        if filters.get("status"):
            papers = [p for p in papers if p.status == filters["status"]]
        
        # Load relationships if needed
        if filters.get("include_authors"):
            papers = [
                await repos.papers.get_with_authors(p.id)
                for p in papers
            ]
        
        return papers
```

## Database Migrations

### Create Initial Schema

```bash
# First time setup
alembic upgrade head
```

### Create New Migration

```bash
# After changing models
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Rollback Migration

```bash
# Undo last migration
alembic downgrade -1
```

### Check Current Version

```bash
alembic current
```

## Error Handling

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

async def safe_create_paper(data: dict):
    try:
        async with get_db() as session:
            repos = get_repositories(session)
            paper = await repos.papers.create(**data)
            return paper
    except IntegrityError as e:
        # Duplicate or constraint violation
        print(f"Data integrity error: {e}")
        return None
    except SQLAlchemyError as e:
        # Database error
        print(f"Database error: {e}")
        return None
    except Exception as e:
        # Other errors
        print(f"Unexpected error: {e}")
        return None
```

## Testing

```python
import pytest
from src.database import get_db, get_repositories

@pytest.mark.asyncio
async def test_create_paper():
    async with get_db() as session:
        repos = get_repositories(session)
        
        paper = await repos.papers.create(
            title="Test Paper",
            abstract="Test abstract",
            published_date=datetime.now()
        )
        
        assert paper.id is not None
        assert paper.title == "Test Paper"
        
        # Cleanup
        await repos.papers.delete(paper.id)
```

## Performance Tips

### 1. Use Bulk Operations

```python
# Bad: Multiple individual inserts
for chunk_data in chunks:
    await repos.chunks.create(**chunk_data)

# Good: Single bulk insert
await repos.chunks.bulk_create(chunks)
```

### 2. Load Relationships Efficiently

```python
# Bad: N+1 queries
papers = await repos.papers.get_all()
for paper in papers:
    authors = await repos.authors.get_by_paper_id(paper.id)

# Good: Eager loading
papers = [
    await repos.papers.get_with_authors(p.id)
    for p in await repos.papers.get_all()
]
```

### 3. Use Pagination

```python
# Get first page
papers = await repos.papers.get_all(limit=20, offset=0)

# Get second page
papers = await repos.papers.get_all(limit=20, offset=20)
```

### 4. Filter at Database Level

```python
# Bad: Load all then filter in Python
all_papers = await repos.papers.get_all()
completed = [p for p in all_papers if p.status == "completed"]

# Good: Filter in database
completed = await repos.papers.get_by_status("completed")
```

This reference covers all the common operations you'll need for working with the database layer!