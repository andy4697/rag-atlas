# Multi-Agent RAG System

A comprehensive multi-agent system for research paper curation and resume generation using RAG (Retrieval-Augmented Generation) technology.

## Features

- **Multi-Agent Architecture**: Specialized agents for different tasks
- **Research Paper Processing**: Automated curation and analysis
- **Resume Generation**: AI-powered resume creation and optimization
- **Vector Search**: Advanced semantic search capabilities
- **Workflow Orchestration**: Automated pipelines with Apache Airflow
- **Observability**: Comprehensive monitoring with Langfuse

## Quick Start

1. **Prerequisites**
   - Docker and Docker Compose
   - Python 3.12+
   - UV package manager

2. **Setup**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd multi-agent-rag-system
   
   # Copy environment file
   cp .env.example .env
   
   # Start the infrastructure
   docker-compose up -d
   ```

3. **Access Services**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Airflow: http://localhost:8080 (admin/admin)
   - OpenSearch Dashboards: http://localhost:5601
   - Langfuse: http://localhost:3000

## Architecture

The system consists of multiple specialized agents:
- **Research Agent**: Paper discovery and analysis
- **Resume Agent**: Resume processing and generation
- **Orchestrator**: Agent coordination and workflow management

## Development

```bash
# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Start development server
uv run python main.py
```

## License

MIT License