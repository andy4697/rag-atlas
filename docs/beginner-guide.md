# Beginner's Guide to the RAG System Database

## What Did I Just Build?

I created a **smart database system** for your RAG (Retrieval-Augmented Generation) application. Think of it like this:

### Before (What you'd have to do manually):
```python
# Lots of complex database code everywhere
import psycopg2
conn = psycopg2.connect("postgresql://...")
cursor = conn.cursor()
cursor.execute("SELECT * FROM papers WHERE title LIKE %s", ("%machine learning%",))
results = cursor.fetchall()
# Convert results to Python objects manually...
# Handle errors manually...
# Close connections manually...
```

### After (What you can do now):
```python
# Simple, clean code
papers = await paper_repository.search_by_title("machine learning")
```

## The 5 Main Components I Built

### 1. 📋 Database Models (`models.py`)
**What it is:** The blueprint for your database tables
**Like:** Designing forms that say "every paper needs a title, author, date"

**Tables created:**
- **Papers** - Research papers from arXiv
- **Authors** - Who wrote the papers
- **Chunks** - Small pieces of paper text for AI search
- **Resumes** - User-uploaded resumes
- **Jobs** - Job descriptions for matching

### 2. 🔧 Base Repository (`base.py`)
**What it is:** A universal toolkit that works with any data type
**Like:** A Swiss Army knife for database operations

**What it gives you:**
```python
# These work for papers, resumes, jobs, anything!
await repo.create(title="New Paper")        # Add new item
await repo.get_by_id(123)                   # Find by ID
await repo.get_all()                        # Get everything
await repo.update(123, title="New Title")   # Change something
await repo.delete(123)                      # Remove item
await repo.search({"status": "completed"})  # Find with filters
```

### 3. 📚 Paper Repository (`papers.py`)
**What it is:** Special tools just for research papers
**Like:** A librarian who specializes in academic papers

**Special powers:**
```python
# Search papers by content
papers = await paper_repo.search_by_title("AI")
papers = await paper_repo.search_by_abstract("neural networks")

# Get papers from specific time periods
recent = await paper_repo.get_recent_papers(days=7)
papers = await paper_repo.get_by_date_range(start_date, end_date)

# Get papers with extra info
paper_with_authors = await paper_repo.get_with_authors(paper_id)
paper_with_chunks = await paper_repo.get_with_chunks(paper_id)
```

### 4. 📄 Resume Repository (`resumes.py`)
**What it is:** Special tools for resumes and job matching
**Like:** An HR assistant who knows resumes inside and out

**Special powers:**
```python
# Manage user resumes
user_resumes = await resume_repo.get_by_user_id("john123")
pending = await resume_repo.get_by_status("processing")

# Job matching magic
matches = await job_match_repo.get_top_matches(resume_id, min_score=0.8)
match = await job_match_repo.create_or_update_match(job_id, resume_id, score=0.85)
```

### 5. 🏭 Repository Factory (`factory.py`)
**What it is:** One place to get all your tools
**Like:** A tool shed where you grab what you need

**How to use:**
```python
# Get access to everything
repos = get_repositories(session)

# Now use any tool you need
papers = await repos.papers.search_by_title("AI")
resumes = await repos.resumes.get_by_user_id("john")
matches = await repos.job_matches.get_top_matches(resume_id)
```

## Real-World Examples

### Example 1: Adding a Research Paper
```python
async def add_new_paper():
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Create the paper
        paper = await repos.papers.create(
            title="Attention Is All You Need",
            abstract="We propose a new simple network architecture...",
            published_date=datetime(2017, 6, 12),
            arxiv_id="1706.03762"
        )
        
        # Add authors
        author = await repos.authors.create(
            name="Ashish Vaswani",
            affiliation="Google Brain"
        )
        
        print(f"Added paper: {paper.title}")
```

### Example 2: Processing a Resume
```python
async def process_resume(user_id, filename):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Create resume record
        resume = await repos.resumes.create(
            user_id=user_id,
            filename=filename,
            file_type="pdf",
            status="processing"
        )
        
        # Later, after AI analysis...
        await repos.resumes.update_analysis_results(
            resume.id,
            analysis_results={
                "completeness_score": 0.85,
                "ats_compatibility": 0.78
            }
        )
        
        print(f"Resume processed for {user_id}")
```

### Example 3: Finding Job Matches
```python
async def find_job_matches(resume_id):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Get top job matches
        matches = await repos.job_matches.get_top_matches(
            resume_id, 
            min_score=0.7
        )
        
        for match in matches:
            print(f"Job: {match.job_description.title}")
            print(f"Score: {match.overall_match_score}")
            print(f"Missing skills: {match.missing_skills}")
```

## Why This Makes Your Life Easier

### ✅ **No More SQL** 
You don't write database queries anymore - just use simple Python methods

### ✅ **Type Safety**
Python will warn you if you make mistakes:
```python
# This will give you an error if 'title' doesn't exist
paper = await repos.papers.get_by_field("title", "AI Paper")
```

### ✅ **Consistent Patterns**
Same methods work for all data types:
```python
papers = await repos.papers.get_all()
resumes = await repos.resumes.get_all()
jobs = await repos.job_descriptions.get_all()
```

### ✅ **Built-in Features**
- Automatic error handling
- Connection management
- Data validation
- Relationship loading

## What You Need to Know

### Dependencies (What's Installed):
- **SQLAlchemy** - Converts Python objects to database tables
- **AsyncPG** - Fast PostgreSQL connections
- **Alembic** - Database version control
- **Pydantic** - Data validation

### Key Concepts:
- **Repository** - A class that handles one type of data
- **Session** - A connection to the database
- **Async/Await** - Modern Python for handling multiple requests
- **Migration** - Updating database structure safely

## Common Patterns You'll Use

### 1. Get Repository Access:
```python
async with get_db() as session:
    repos = get_repositories(session)
    # Use repos here...
```

### 2. Create New Records:
```python
item = await repos.papers.create(title="...", abstract="...")
```

### 3. Search and Filter:
```python
results = await repos.papers.search_by_title("machine learning")
filtered = await repos.papers.get_by_filters({"status": "completed"})
```

### 4. Update Records:
```python
updated = await repos.papers.update(paper_id, status="completed")
```

## What's Next?

Now that you have this solid foundation, you can build:

1. **API Endpoints** - Web interface to your data
2. **Paper Ingestion** - Automatically download papers from arXiv
3. **Resume Analysis** - AI-powered resume enhancement
4. **Job Matching** - Smart compatibility scoring

The complex database work is done - now you can focus on the exciting AI features!

## Need Help?

Check out:
- `examples/repository_usage.py` - Working examples
- `docs/database-explained.md` - Detailed explanations
- The actual repository files - they have lots of comments

Remember: You don't need to understand every line of code I wrote. Just use the simple methods like `create()`, `get_all()`, and `search_by_title()` to build your features!