# Code Walkthrough - What I Built and Why

## Overview
I built a **Repository Pattern** for your database. Think of it as a smart assistant that handles all the boring database stuff so you can focus on the cool features.

## File-by-File Breakdown

### 1. `src/database/models.py` - Database Tables Definition

**What it does:** Defines the structure of your database tables
**Why it exists:** PostgreSQL needs to know what columns each table has
**Dependencies:** SQLAlchemy, Enums from your Pydantic models

**Key Tables Created:**
- `papers` - Stores research papers
- `authors` - Stores paper authors  
- `chunks` - Stores text pieces from papers
- `resumes` - Stores uploaded resumes
- `job_descriptions` - Stores job postings
- `job_matches` - Stores resume-job matching results

**Example:**
```python
class Paper(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    abstract = Column(Text, nullable=False)
    # ... more columns
```

### 2. `src/database/connection.py` - Database Connection Setup

**What it does:** Manages connections to PostgreSQL
**Why it exists:** Your app needs to connect to the database safely
**Dependencies:** SQLAlchemy, AsyncPG, your settings

**Key Features:**
- Async database connections (faster)
- Connection pooling (handles multiple users)
- Session management (keeps data consistent)

### 3. `src/database/repositories/base.py` - The Universal Template

**What it does:** Provides common database operations for any data type
**Why it exists:** Avoid writing the same CRUD code over and over
**Dependencies:** SQLAlchemy, Python typing

**Key Methods:**
```python
async def create(**kwargs)           # Add new record
async def get_by_id(id)             # Find by ID
async def get_all()                 # Get all records
async def update(id, **kwargs)      # Update record
async def delete(id)                # Delete record
async def get_by_filters(filters)   # Search with conditions
```

**Real Example:**
```python
# This works for ANY type of data (papers, resumes, etc.)
repository = BaseRepository(Paper, session)
paper = await repository.create(title="My Paper", abstract="...")
```

### 4. `src/database/repositories/papers.py` - Paper-Specific Operations

**What it does:** Specialized operations for research papers
**Why it exists:** Papers need special search and organization features
**Dependencies:** Base repository, SQLAlchemy

**Special Features:**
- Search by title or abstract
- Filter by date ranges
- Get papers with their authors
- Get papers with text chunks
- Update processing status

**Example:**
```python
# Find papers about "machine learning" from last month
papers = await paper_repo.search_by_title("machine learning")
recent = await paper_repo.get_recent_papers(days=30)
```

### 5. `src/database/repositories/resumes.py` - Resume-Specific Operations

**What it does:** Specialized operations for resumes and job matching
**Why it exists:** Resumes need parsing, analysis, and job matching features
**Dependencies:** Base repository, SQLAlchemy

**Special Features:**
- Get resumes by user
- Track processing status
- Store analysis results
- Match with job descriptions
- Calculate compatibility scores

**Example:**
```python
# Get all resumes for a user and find job matches
user_resumes = await resume_repo.get_by_user_id("user123")
matches = await job_match_repo.get_top_matches(resume_id, min_score=0.8)
```

### 6. `src/database/repositories/factory.py` - The Manager Class

**What it does:** Provides easy access to all repositories
**Why it exists:** One place to get all your database helpers
**Dependencies:** All repository classes

**How to use:**
```python
# Get all repositories at once
repos = get_repositories(session)

# Now use any repository
papers = await repos.papers.get_all()
resumes = await repos.resumes.get_by_user_id("user123")
matches = await repos.job_matches.get_top_matches(resume_id)
```

### 7. `alembic/` - Database Migration System

**What it does:** Manages database schema changes over time
**Why it exists:** Safely update database structure without losing data
**Dependencies:** Alembic, SQLAlchemy

**Key Files:**
- `alembic.ini` - Configuration
- `env.py` - Environment setup
- `versions/` - Migration scripts

**How it works:**
```bash
# Create tables for the first time
alembic upgrade head

# Later, when you change models, create new migration
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## How Everything Connects

```
Your Application Code
        ↓
Repository Factory (factory.py)
        ↓
Specific Repositories (papers.py, resumes.py)
        ↓
Base Repository (base.py)
        ↓
SQLAlchemy Models (models.py)
        ↓
Database Connection (connection.py)
        ↓
PostgreSQL Database
```

## Dependencies Explained

### Core Dependencies:
1. **SQLAlchemy** - Object-Relational Mapping (converts Python objects to database tables)
2. **AsyncPG** - Async PostgreSQL driver (fast database connections)
3. **Alembic** - Database migration tool (version control for database schema)
4. **Pydantic** - Data validation (ensures data is correct format)

### Why Async?
- **Faster** - Can handle multiple requests at once
- **Scalable** - Supports many users simultaneously
- **Modern** - Best practice for web applications

## What You Can Do Now

### Add a Paper:
```python
async with get_db() as session:
    repos = get_repositories(session)
    paper = await repos.papers.create(
        title="My Research Paper",
        abstract="This paper discusses...",
        published_date=datetime.now()
    )
```

### Search Papers:
```python
# Find papers by title
papers = await repos.papers.search_by_title("machine learning")

# Get recent papers
recent = await repos.papers.get_recent_papers(days=7)

# Get paper with authors
paper_with_authors = await repos.papers.get_with_authors(paper_id)
```

### Upload and Analyze Resume:
```python
# Create resume record
resume = await repos.resumes.create(
    user_id="user123",
    filename="john_doe_resume.pdf",
    file_size=245760,
    file_type="pdf"
)

# Update with analysis results
await repos.resumes.update_analysis_results(
    resume.id,
    analysis_results={"completeness_score": 0.85},
    enhancement_suggestions=[...]
)
```

## Benefits of This Approach

1. **Beginner Friendly** - Simple methods like `create()`, `get_all()`
2. **Type Safe** - Python will warn you about mistakes
3. **Reusable** - Same patterns work for all data types
4. **Testable** - Easy to write tests for each repository
5. **Maintainable** - Changes in one place affect everywhere
6. **Scalable** - Async support for high performance

## What's Next?

Now that the database foundation is solid, you can build:
1. **API endpoints** - Web interface to your data
2. **Paper ingestion** - Automatically download and process papers
3. **Resume analysis** - AI-powered resume enhancement
4. **Job matching** - Smart resume-job compatibility

The hard database work is done - now for the fun stuff!