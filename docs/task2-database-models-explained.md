# Task 2: Database Models & Repository Pattern Explained

## What Did We Build?

Task 2 created the **data layer** of your RAG system. Think of it as building a smart filing system that knows how to store and find research papers, resumes, and job descriptions.

## The Big Picture

```
Your Application
       ↓
Repository Layer (Smart Assistants)
       ↓
SQLAlchemy Models (Filing System Rules)
       ↓
PostgreSQL Database (The Actual Files)
```

## Three Main Parts

### Part 1: Pydantic Models (Task 2.1) - The Forms
**What they are:** Templates that define what data looks like
**Like:** Forms you fill out - they tell you what information is required

**Example:**
```python
class Paper(BaseModel):
    title: str                    # Required text
    abstract: str                 # Required text
    published_date: datetime      # Required date
    citation_count: int = 0       # Optional number, defaults to 0
```

**Why they matter:**
- Validate data before it goes into the database
- Catch errors early (like missing required fields)
- Auto-generate API documentation
- Type safety in your code

### Part 2: Database Schema (Task 2.2) - The Filing Cabinet
**What it is:** The actual structure of your database tables
**Like:** Designing the drawers and labels in your filing cabinet

**Tables created:**
1. **papers** - Research papers from arXiv
2. **authors** - Who wrote the papers
3. **chunks** - Small pieces of paper text for AI search
4. **resumes** - User-uploaded resumes
5. **job_descriptions** - Job postings
6. **job_matches** - Resume-job compatibility scores

**Why it matters:**
- Organized data storage
- Fast searches with indexes
- Relationships between data (papers have authors)
- Data integrity (can't delete a paper if it has chunks)

### Part 3: Repository Pattern (Task 2.3) - The Smart Assistants
**What they are:** Helper classes that make database operations simple
**Like:** Personal assistants who know exactly how to file and find things

**What they do:**
```python
# Instead of complex SQL:
SELECT * FROM papers WHERE title LIKE '%AI%' AND published_date > '2024-01-01'

# You just write:
papers = await paper_repo.search_by_title("AI")
```

## Real-World Example: Adding a Research Paper

### The Old Way (Without Our System):
```python
# Step 1: Connect to database
conn = psycopg2.connect("postgresql://...")
cursor = conn.cursor()

# Step 2: Insert paper
cursor.execute("""
    INSERT INTO papers (title, abstract, published_date, status)
    VALUES (%s, %s, %s, %s)
    RETURNING id
""", ("My Paper", "Abstract...", "2024-01-01", "pending"))
paper_id = cursor.fetchone()[0]

# Step 3: Insert authors
for author_name in authors:
    cursor.execute("""
        INSERT INTO authors (name) VALUES (%s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
    """, (author_name,))
    author_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO paper_authors (paper_id, author_id, author_order)
        VALUES (%s, %s, %s)
    """, (paper_id, author_id, order))

# Step 4: Commit and handle errors
try:
    conn.commit()
except Exception as e:
    conn.rollback()
    # Handle error...
finally:
    cursor.close()
    conn.close()
```

### The New Way (With Our System):
```python
# That's it! Everything else is handled automatically
async with get_db() as session:
    repos = get_repositories(session)
    
    paper = await repos.papers.create(
        title="My Paper",
        abstract="Abstract...",
        published_date=datetime(2024, 1, 1)
    )
    
    for author_name in authors:
        author = await repos.authors.get_or_create(name=author_name)
```

## What Each Component Does

### 1. Pydantic Models (`src/models/`)

#### `papers.py` - Research Paper Models
**What's inside:**
- `Paper` - Complete paper with metadata
- `Author` - Paper author information
- `Chunk` - Text segments for AI search
- `PaperSearchRequest` - How to search for papers
- `PaperSearchResponse` - Search results format

**Example:**
```python
class Paper(TimestampMixin):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=500)
    abstract: str = Field(..., min_length=10, max_length=5000)
    authors: List[Author] = Field(..., min_items=1)
    status: PaperStatus = PaperStatus.PENDING
```

#### `resumes.py` - Resume and Job Models
**What's inside:**
- `Resume` - User resume with analysis
- `JobDescription` - Job posting details
- `JobMatch` - Resume-job compatibility
- `ParsedResumeData` - Structured resume content
- `AnalysisResult` - Resume quality scores

### 2. Database Models (`src/database/models.py`)

**SQLAlchemy Tables:**
```python
class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    abstract = Column(Text, nullable=False)
    status = Column(Enum(PaperStatus), default=PaperStatus.PENDING)
    
    # Relationships
    chunks = relationship("Chunk", back_populates="paper")
    paper_authors = relationship("PaperAuthor", back_populates="paper")
```

**Key Features:**
- Automatic timestamps (created_at, updated_at)
- Foreign key relationships
- Indexes for fast searches
- Cascade deletes (delete paper → delete chunks)

### 3. Repository Classes (`src/database/repositories/`)

#### Base Repository (`base.py`)
**Universal operations for any data type:**
```python
# Works with papers, resumes, jobs, anything!
await repo.create(**data)              # Add new
await repo.get_by_id(123)             # Find by ID
await repo.get_all(limit=10)          # Get multiple
await repo.update(123, title="New")   # Change
await repo.delete(123)                # Remove
await repo.count(filters={...})       # Count
```

#### Paper Repository (`papers.py`)
**Specialized for research papers:**
```python
# Search operations
await paper_repo.search_by_title("machine learning")
await paper_repo.search_by_abstract("neural networks")
await paper_repo.get_by_date_range(start, end)
await paper_repo.get_recent_papers(days=7)

# Relationship loading
await paper_repo.get_with_authors(paper_id)
await paper_repo.get_with_chunks(paper_id)

# Status management
await paper_repo.update_processing_status(paper_id, "completed")
```

#### Resume Repository (`resumes.py`)
**Specialized for resumes:**
```python
# User operations
await resume_repo.get_by_user_id("user123")
await resume_repo.get_by_status("processing")

# Analysis operations
await resume_repo.update_parsed_data(resume_id, parsed_data)
await resume_repo.update_analysis_results(resume_id, analysis)

# Job matching
await job_match_repo.get_top_matches(resume_id, min_score=0.8)
await job_match_repo.create_or_update_match(job_id, resume_id, score=0.85)
```

### 4. Database Migrations (`alembic/`)

**What it does:** Version control for your database structure
**Like:** Git for your database schema

**Key files:**
- `alembic.ini` - Configuration
- `env.py` - Environment setup
- `versions/` - Migration scripts

**How to use:**
```bash
# Create tables for first time
alembic upgrade head

# Later, when you change models
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## Benefits You Get

### 1. **Type Safety**
```python
# Python will warn you about mistakes
paper = await repos.papers.create(
    title=123  # ERROR: title must be string, not int
)
```

### 2. **Automatic Validation**
```python
# Pydantic catches bad data
paper = Paper(
    title="",  # ERROR: title must be at least 1 character
    abstract="Short"  # ERROR: abstract must be at least 10 characters
)
```

### 3. **Clean Code**
```python
# Before: 50 lines of SQL and error handling
# After: 2 lines of clean Python
paper = await repos.papers.create(title="...", abstract="...")
```

### 4. **Reusable Operations**
```python
# Same patterns work everywhere
papers = await repos.papers.get_all()
resumes = await repos.resumes.get_all()
jobs = await repos.job_descriptions.get_all()
```

### 5. **Easy Testing**
```python
# Mock the repository in tests
mock_repo = Mock(spec=PaperRepository)
mock_repo.get_by_id.return_value = fake_paper
```

## Data Flow Example

### Uploading and Processing a Resume:

```
1. User uploads PDF
   ↓
2. API validates file (Pydantic)
   ↓
3. Create resume record (Repository)
   ↓
4. Store in database (SQLAlchemy)
   ↓
5. AI processes resume
   ↓
6. Update with results (Repository)
   ↓
7. Match with jobs (Repository)
   ↓
8. Return results to user
```

**Code:**
```python
# Step 1-4: Upload
resume = await repos.resumes.create(
    user_id="user123",
    filename="resume.pdf",
    file_type="pdf",
    status="processing"
)

# Step 5-6: Process
parsed_data = await ai_parse_resume(resume.file_path)
await repos.resumes.update_parsed_data(resume.id, parsed_data)

analysis = await ai_analyze_resume(parsed_data)
await repos.resumes.update_analysis_results(resume.id, analysis)

# Step 7-8: Match
matches = await repos.job_matches.get_top_matches(resume.id)
return {"resume": resume, "matches": matches}
```

## Common Patterns

### Pattern 1: Create with Relationships
```python
# Create paper with authors
paper = await repos.papers.create(title="...", abstract="...")

for author_name in ["Dr. Smith", "Dr. Jones"]:
    author = await repos.authors.get_or_create(name=author_name)
    # Link paper and author...
```

### Pattern 2: Search and Filter
```python
# Find papers about AI from last month
papers = await repos.papers.search_by_title("AI")
recent = [p for p in papers if p.published_date > last_month]
```

### Pattern 3: Update Status
```python
# Track processing progress
await repos.papers.update_processing_status(
    paper_id,
    "processing",
    {"step": "downloading"}
)

# ... do work ...

await repos.papers.update_processing_status(
    paper_id,
    "completed",
    {"chunks_created": 42}
)
```

## What You Can Build Now

With this foundation, you can:

1. **Store Research Papers**
   - Download from arXiv
   - Extract text and metadata
   - Create searchable chunks

2. **Manage Resumes**
   - Upload and parse resumes
   - Analyze quality and completeness
   - Generate enhancement suggestions

3. **Match Jobs**
   - Compare resumes with job descriptions
   - Calculate compatibility scores
   - Identify skill gaps

4. **Build APIs**
   - Create endpoints using repositories
   - Return validated data
   - Handle errors gracefully

## Summary

Task 2 gave you:
- ✅ **Pydantic Models** - Data validation and API schemas
- ✅ **Database Schema** - Organized, indexed tables
- ✅ **Repository Pattern** - Clean, reusable database operations
- ✅ **Migration System** - Safe database updates
- ✅ **Type Safety** - Catch errors before runtime

You now have a **professional data layer** that's:
- Easy to use
- Hard to break
- Simple to test
- Ready to scale