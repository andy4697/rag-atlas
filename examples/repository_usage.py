"""Example usage of database repositories."""

import asyncio
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database import get_db, get_repositories
from src.models.papers import PaperStatus


async def example_paper_operations():
    """Example paper repository operations."""
    async for session in get_db():
        repos = get_repositories(session)

        # Create a new paper
        paper = await repos.papers.create(
            title="Example Research Paper",
            abstract="This is an example abstract for demonstration purposes.",
            published_date=datetime.utcnow(),
            status=PaperStatus.PENDING
        )
        print(f"Created paper: {paper.id} - {paper.title}")

        # Create an author
        author = await repos.authors.create(
            name="Dr. Jane Smith",
            affiliation="Example University",
            email="jane.smith@example.edu"
        )
        print(f"Created author: {author.id} - {author.name}")

        # Search papers by title
        papers = await repos.papers.search_by_title("Example")
        print(f"Found {len(papers)} papers with 'Example' in title")

        # Get paper with authors
        paper_with_authors = await repos.papers.get_with_authors(paper.id)
        if paper_with_authors:
            print(f"Paper {paper_with_authors.title} has {len(paper_with_authors.paper_authors)} authors")

        # Update paper status
        updated_paper = await repos.papers.update_processing_status(
            paper.id,
            PaperStatus.COMPLETED,
            {"processing_time": 120.5}
        )
        print(f"Updated paper status to: {updated_paper.status}")

        # Create chunks for the paper
        chunks_data = [
            {
                "paper_id": paper.id,
                "content": "This is the first chunk of content.",
                "chunk_index": 0,
                "section_type": "introduction",
                "token_count": 10,
                "char_count": 35
            },
            {
                "paper_id": paper.id,
                "content": "This is the second chunk of content.",
                "chunk_index": 1,
                "section_type": "methods",
                "token_count": 10,
                "char_count": 36
            }
        ]

        chunks = await repos.chunks.bulk_create(chunks_data)
        print(f"Created {len(chunks)} chunks for paper")

        # Get chunks for paper
        paper_chunks = await repos.chunks.get_by_paper_id(paper.id)
        print(f"Paper has {len(paper_chunks)} chunks")

        # Search chunks by content
        found_chunks = await repos.chunks.search_content("first chunk")
        print(f"Found {len(found_chunks)} chunks with 'first chunk'")

        await session.commit()


async def example_resume_operations():
    """Example resume repository operations."""
    async for session in get_db():
        repos = get_repositories(session)

        # Create a resume
        resume = await repos.resumes.create(
            user_id="user123",
            filename="john_doe_resume.pdf",
            file_size=245760,
            file_type="pdf",
            status="pending"
        )
        print(f"Created resume: {resume.id} - {resume.filename}")

        # Create a job description
        job = await repos.job_descriptions.create(
            title="Senior Software Engineer",
            company="Tech Corp",
            location="San Francisco, CA",
            employment_type="full-time",
            experience_level="senior",
            description="We are looking for a senior software engineer...",
            required_skills=["Python", "React", "PostgreSQL"],
            salary_range="$120,000 - $160,000"
        )
        print(f"Created job: {job.id} - {job.title}")

        # Create a job match
        match = await repos.job_matches.create_or_update_match(
            job_id=job.id,
            resume_id=resume.id,
            overall_match_score=0.85,
            skill_match_score=0.90,
            experience_match_score=0.80,
            matching_skills=["Python", "PostgreSQL"],
            missing_skills=["React"],
            recommendations=["Add React experience", "Highlight Python projects"]
        )
        print(f"Created job match with score: {match.overall_match_score}")

        # Get top matches for resume
        top_matches = await repos.job_matches.get_top_matches(resume.id, min_score=0.7)
        print(f"Found {len(top_matches)} high-quality matches")

        # Update resume analysis
        updated_resume = await repos.resumes.update_analysis_results(
            resume.id,
            analysis_results={
                "completeness_score": 0.85,
                "ats_compatibility_score": 0.78,
                "strengths": ["Strong technical skills", "Clear experience progression"]
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
        print(f"Updated resume analysis for: {updated_resume.filename}")

        await session.commit()


async def main():
    """Run example operations."""
    print("=== Paper Repository Examples ===")
    await example_paper_operations()

    print("\n=== Resume Repository Examples ===")
    await example_resume_operations()

    print("\nRepository examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
