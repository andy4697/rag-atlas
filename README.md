# 🤖 Multi-Agent RAG System

> An intelligent system that automatically curates research papers from arXiv and generates AI-enhanced resumes with job matching capabilities.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 What Does This Do?

This system combines multiple AI agents to:

1. **📚 Research Paper Management**
   - Automatically download papers from arXiv
   - Extract and chunk text for AI search
   - Semantic search across paper content
   - Generate research summaries

2. **📄 Resume Enhancement**
   - Parse resumes (PDF, DOCX, TXT)
   - Analyze completeness and ATS compatibility
   - Generate improvement suggestions
   - Match resumes with job descriptions

3. **🎯 Job Matching**
   - Calculate resume-job compatibility scores
   - Identify skill gaps
   - Provide customization recommendations
   - Generate tailored resumes for specific jobs

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop)
- **Python 3.12+** - [Download here](https://www.python.org/downloads/)
- **UV Package Manager** - [Install guide](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd rag-atlas

# Copy environment configuration
cp .env.example .env

# Edit .env with your settings (optional for local development)
```

### 2. Start All Services

```bash
# Start all infrastructure services
docker compose up -d

# Wait 2-3 minutes for all services to be healthy
docker compose ps
```

### 3. Verify Setup

Open your browser and check:

- ✅ **API Documentation**: http://localhost:8000/docs
- ✅ **API Health**: http://localhost:8000/api/v1/health/
- ✅ **Airflow Dashboard**: http://localhost:8080 (admin/admin)
- ✅ **OpenSearch Dashboards**: http://localhost:5601
- ✅ **Langfuse Observability**: http://localhost:3000

### 4. Run the Setup Notebook

```bash
# Open Jupyter
jupyter notebook notebooks/01_setup.ipynb

# Run all cells to verify everything works
```

## 📖 Documentation

### For Beginners
Start here if you're new to the project:

- **[Beginner's Guide](docs/beginner-guide.md)** - Complete introduction to the system
- **[Database Explained](docs/database-explained.md)** - Understanding the data layer
- **[Quick Reference](docs/quick-reference.md)** - Copy-paste code examples

### Technical Documentation
Deep dives into implementation:

- **[Task 1: Project Setup](docs/task1-project-setup-explained.md)** - Foundation and infrastructure
- **[Task 2: Database Models](docs/task2-database-models-explained.md)** - Data layer architecture
- **[Code Walkthrough](docs/code-walkthrough.md)** - File-by-file breakdown

### Quick References
Copy-paste ready examples:

- **[Database Operations](docs/task2-database-models-reference.md)** - All CRUD operations
- **[API Examples](docs/quick-reference.md)** - Common patterns

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI REST API                        │
│              (http://localhost:8000/docs)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Agent Orchestrator                        │
│         (Coordinates Research & Resume Agents)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
┌──────────────────┐                  ┌──────────────────┐
│  Research Agent  │                  │   Resume Agent   │
│                  │                  │                  │
│ • arXiv Search   │                  │ • Parse Resumes  │
│ • PDF Download   │                  │ • Analyze Quality│
│ • Text Chunking  │                  │ • Match Jobs     │
│ • Embeddings     │                  │ • Generate Docs  │
└──────────────────┘                  └──────────────────┘
        ↓                                       ↓
┌─────────────────────────────────────────────────────────────┐
│                    Repository Layer                         │
│         (Clean database operations via repositories)        │
└─────────────────────────────────────────────────────────────┘
        ↓                                       ↓
┌──────────────────┐                  ┌──────────────────┐
│   PostgreSQL     │                  │   OpenSearch     │
│                  │                  │                  │
│ • Papers         │                  │ • Vector Search  │
│ • Resumes        │                  │ • Full-text      │
│ • Job Matches    │                  │ • Embeddings     │
└──────────────────┘                  └──────────────────┘
```

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** - Modern async web framework
- **SQLAlchemy 2.0** - Database ORM with async support
- **Pydantic** - Data validation and settings management

### Data Storage
- **PostgreSQL** - Primary relational database
- **OpenSearch** - Vector and full-text search
- **Redis** - Caching and session storage

### AI & ML
- **Ollama** - Local LLM inference
- **Sentence Transformers** - Text embeddings
- **Langfuse** - LLM observability and monitoring

### Workflow & Orchestration
- **Apache Airflow** - Workflow automation
- **Docker Compose** - Service orchestration

### Development Tools
- **UV** - Fast Python package manager
- **Ruff** - Code formatter and linter
- **Pytest** - Testing framework
- **Alembic** - Database migrations

## 📁 Project Structure

```
rag-atlas/
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   │   ├── main.py              # App factory
│   │   ├── routes/              # API endpoints
│   │   └── middleware.py        # Request processing
│   ├── agents/                   # AI agents
│   │   ├── base.py              # Base agent class
│   │   ├── research_agent.py   # Paper processing
│   │   └── resume_agent.py     # Resume processing
│   ├── database/                 # Data layer
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── connection.py        # DB connections
│   │   └── repositories/        # Data access layer
│   ├── models/                   # Pydantic models
│   │   ├── papers.py            # Paper schemas
│   │   └── resumes.py           # Resume schemas
│   ├── core/                     # Core utilities
│   │   ├── config.py            # Configuration
│   │   └── logging.py           # Logging setup
│   └── services/                 # Business logic
├── tests/                        # Test suite
├── docs/                         # Documentation
├── notebooks/                    # Jupyter notebooks
├── alembic/                      # Database migrations
├── airflow/                      # Airflow DAGs
│   └── dags/                    # Workflow definitions
├── compose.yml                   # Docker services
├── pyproject.toml               # Project config
└── README.md                    # This file
```

## 💻 Development

### Install Dependencies

```bash
# Install UV if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync --dev
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/

# Run specific test file
uv run pytest tests/test_database.py
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Check current version
alembic current
```

### Start Development Server

```bash
# Start FastAPI with hot reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Configuration

### Environment Variables

Key settings in `.env`:

```bash
# Application
ENV=development
DEBUG=true

# Database
DATABASE_URL=postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_db

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenSearch
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200

# LLM
OLLAMA_URL=http://localhost:11434
OPENAI_API_KEY=your-key-here  # Optional

# Langfuse (Optional)
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_PUBLIC_KEY=your-public-key
```

### Docker Services

All services are defined in `compose.yml`:

| Service | Port | Purpose |
|---------|------|---------|
| API | 8000 | FastAPI REST API |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Caching |
| OpenSearch | 9200 | Vector search |
| OpenSearch Dashboards | 5601 | Search UI |
| Ollama | 11434 | Local LLM |
| Airflow | 8080 | Workflow UI |
| Langfuse | 3000 | Observability |

## 📝 Usage Examples

### Add a Research Paper

```python
from src.database import get_db, get_repositories
from datetime import datetime

async def add_paper():
    async with get_db() as session:
        repos = get_repositories(session)
        
        paper = await repos.papers.create(
            title="Attention Is All You Need",
            abstract="We propose a new simple network architecture...",
            arxiv_id="1706.03762",
            published_date=datetime(2017, 6, 12)
        )
        
        print(f"Added paper: {paper.title}")
```

### Search Papers

```python
async def search_papers(query: str):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Search by title
        papers = await repos.papers.search_by_title(query)
        
        # Get recent papers
        recent = await repos.papers.get_recent_papers(days=7)
        
        return papers
```

### Process a Resume

```python
async def process_resume(user_id: str, file_path: str):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Create resume record
        resume = await repos.resumes.create(
            user_id=user_id,
            filename=os.path.basename(file_path),
            file_type="pdf",
            file_size=os.path.getsize(file_path)
        )
        
        # Process and analyze
        # ... AI processing here ...
        
        # Update with results
        await repos.resumes.update_analysis_results(
            resume.id,
            analysis_results={"completeness_score": 0.85},
            enhancement_suggestions=[...]
        )
        
        return resume
```

### Match Resume with Jobs

```python
async def find_matches(resume_id: int):
    async with get_db() as session:
        repos = get_repositories(session)
        
        # Get top job matches
        matches = await repos.job_matches.get_top_matches(
            resume_id,
            min_score=0.7,
            limit=10
        )
        
        for match in matches:
            print(f"Job: {match.job_description.title}")
            print(f"Score: {match.overall_match_score}")
            print(f"Missing skills: {match.missing_skills}")
```

## 🧪 Testing

### Run Setup Verification

```bash
# Open the setup notebook
jupyter notebook notebooks/01_setup.ipynb

# Or run the test script
python tests/test_infrastructure.py
```

### Test Database Connection

```python
import asyncio
from src.database import get_db, get_repositories

async def test_db():
    async with get_db() as session:
        repos = get_repositories(session)
        count = await repos.papers.count()
        print(f"Papers in database: {count}")

asyncio.run(test_db())
```

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check service status
docker compose ps

# View logs for specific service
docker compose logs api
docker compose logs postgres
docker compose logs opensearch

# Restart all services
docker compose restart
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Test connection
docker exec -it rag-postgres psql -U rag_user -d rag_db -c "SELECT 1"

# Reset database
docker compose down -v
docker compose up -d
```

### Port Conflicts

If ports are already in use:

```bash
# Check what's using a port (e.g., 8000)
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change ports in compose.yml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - Modern web framework
- **SQLAlchemy** - Powerful ORM
- **Ollama** - Local LLM inference
- **OpenSearch** - Search and analytics
- **Apache Airflow** - Workflow orchestration

## 📞 Support

- **Documentation**: Check the `docs/` folder
- **Issues**: Open an issue on GitHub
- **Questions**: Start a discussion

## 🗺️ Roadmap

- [x] Project setup and infrastructure
- [x] Database models and repository pattern
- [ ] Airflow data ingestion pipeline
- [ ] Paper parsing with GROBID/Docling
- [ ] Vector embeddings and search
- [ ] Research agent implementation
- [ ] Resume agent implementation
- [ ] FastAPI endpoints
- [ ] React frontend
- [ ] Langfuse observability
- [ ] Production deployment

---

**Built with ❤️ using FastAPI, SQLAlchemy, and modern Python**