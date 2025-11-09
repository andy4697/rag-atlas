# Database Layer Explained (For Beginners)

## What is this database stuff?

Think of a database like a digital filing cabinet. Instead of paper files, we store information about research papers, resumes, and job descriptions. The code I wrote helps your Python application talk to this filing cabinet.

## The Big Picture

```
Your Python App
       ↓
Repository Layer (What I built)
       ↓
SQLAlchemy (Database toolkit)
       ↓
PostgreSQL Database (The actual filing cabinet)
```

## What Each File Does

### 1. `src/database/models.py` - The Blueprint
**What it is:** Defines what our "filing cabinet drawers" look like
**Think of it as:** Creating forms that say "every paper must have a title, author, date, etc."

**Example:**
```python
class Paper:
    title = "Research Paper Title"
    author = "Dr. Smith"
    published_date = "2024-01-15"
```

### 2. `src/database/repositories/base.py` - The Universal Helper
**What it is:** A template that provides common operations for any type of data
**Think of it as:** A universal remote control that works with any drawer in your filing cabinet

**What it can do:**
- Create new records (add a new paper)
- Find records (search for papers by title)
- Update records (change paper information)
- Delete records (remove papers)

**Simple example:**
```python
# Instead of writing complex database code every time:
papers = repository.get_all()  # Get all papers
paper = repository.get_by_id(1)  # Get paper with ID 1
```

### 3. `src/database/repositories/papers.py` - Paper-Specific Helper
**What it is:** Specialized tools for working with research papers
**Think of it as:** A librarian who knows exactly how to organize and find academic papers

**What it can do:**
- Search papers by title: "Find all papers about 'machine learning'"
- Search by date: "Show me papers from last month"
- Get paper with authors: "Give me the paper and tell me who wrote it"

### 4. `src/database/repositories/resumes.py` - Resume-Specific Helper
**What it is:** Specialized tools for working with resumes and job descriptions
**Think of it as:** An HR assistant who knows how to organize resumes and match them with jobs

**What it can do:**
- Find all resumes for a user
- Match resumes with job descriptions
- Track resume processing status

### 5. `src/database/repositories/factory.py` - The Manager
**What it is:** A single place to get all your helpers
**Think of it as:** A receptionist who directs you to the right department

**Simple example:**
```python
repos = get_repositories(session)
papers = repos.papers.get_all()  # Get paper helper
resumes = repos.resumes.get_all()  # Get resume helper
```

## Why This Pattern?

### Without Repositories (Bad way):
```python
# Messy, repeated database code everywhere
result = session.execute("SELECT * FROM papers WHERE title LIKE '%AI%'")
papers = result.fetchall()
# Convert to objects manually...
# Handle errors manually...
# Repeat this code in every file...
```

### With Repositories (Clean way):
```python
# Simple, clean, reusable
papers = paper_repository.search_by_title("AI")
```

## Dependencies Explained

### What you need installed:
1. **SQLAlchemy** - Translates Python code to database language
2. **AsyncPG** - Connects to PostgreSQL database
3. **Pydantic** - Validates data (makes sure papers have titles, etc.)

### How they work together:
```
Your Code → Repository → SQLAlchemy → AsyncPG → PostgreSQL
```

## Real-World Example

Let's say you want to add a new research paper:

### The Old Way (Complex):
```python
# You'd need to write SQL, handle connections, manage errors...
connection = get_database_connection()
cursor = connection.cursor()
cursor.execute(
    "INSERT INTO papers (title, abstract, published_date) VALUES (%s, %s, %s)",
    ("My Paper", "Abstract text", "2024-01-01")
)
connection.commit()
# Handle errors, close connections, etc.
```

### The New Way (Simple):
```python
# Just use the repository!
paper = await paper_repository.create(
    title="My Paper",
    abstract="Abstract text", 
    published_date=datetime(2024, 1, 1)
)
```

## What This Gives You

1. **Less Code** - Don't repeat database operations
2. **Fewer Bugs** - Tested, reusable functions
3. **Easier Changes** - Change database logic in one place
4. **Better Organization** - Each type of data has its own helper
5. **Type Safety** - Python tells you if you make mistakes

## Next Steps

Now that you have this foundation, you can:
1. Add new papers to the database
2. Search and filter papers
3. Upload and analyze resumes
4. Match resumes with job descriptions

The complex part is done - now you can focus on the fun features!