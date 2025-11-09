"""Repository classes for resume-related entities."""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Resume, JobDescription, JobMatch
from .base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    """Repository for Resume entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(Resume, session)

    async def get_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Resume]:
        """Get resumes for a specific user."""
        return await self.get_by_filters(
            {"user_id": user_id},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )

    async def get_by_status(
        self,
        status: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Resume]:
        """Get resumes by processing status."""
        return await self.get_by_filters(
            {"status": status},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )

    async def get_with_matches(self, resume_id: int) -> Optional[Resume]:
        """Get resume with job matches loaded."""
        result = await self.session.execute(
            select(Resume)
            .options(selectinload(Resume.job_matches))
            .where(Resume.id == resume_id)
        )
        return result.scalar_one_or_none()

    async def update_processing_status(
        self,
        resume_id: int,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Resume]:
        """Update resume processing status and metadata."""
        update_data = {"status": status}
        if metadata:
            update_data["processing_metadata"] = metadata

        return await self.update(resume_id, **update_data)

    async def update_parsed_data(
        self,
        resume_id: int,
        parsed_data: Dict[str, Any]
    ) -> Optional[Resume]:
        """Update resume parsed data."""
        return await self.update(resume_id, parsed_data=parsed_data)

    async def update_analysis_results(
        self,
        resume_id: int,
        analysis_results: Dict[str, Any],
        enhancement_suggestions: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Resume]:
        """Update resume analysis results and enhancement suggestions."""
        update_data = {"analysis_results": analysis_results}
        if enhancement_suggestions:
            update_data["enhancement_suggestions"] = enhancement_suggestions

        return await self.update(resume_id, **update_data)

    async def get_recent_resumes(
        self,
        days: int = 30,
        limit: int = 50
    ) -> List[Resume]:
        """Get resumes created in the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = await self.session.execute(
            select(Resume)
            .where(Resume.created_at >= cutoff_date)
            .order_by(desc(Resume.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def search_by_filename(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Resume]:
        """Search resumes by filename."""
        result = await self.session.execute(
            select(Resume)
            .where(Resume.filename.ilike(f"%{query}%"))
            .order_by(desc(Resume.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_file_type(
        self,
        file_type: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Resume]:
        """Get resumes by file type."""
        return await self.get_by_filters(
            {"file_type": file_type},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )


class JobDescriptionRepository(BaseRepository[JobDescription]):
    """Repository for JobDescription entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(JobDescription, session)

    async def search_by_title(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[JobDescription]:
        """Search job descriptions by title."""
        result = await self.session.execute(
            select(JobDescription)
            .where(JobDescription.title.ilike(f"%{query}%"))
            .order_by(desc(JobDescription.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def search_by_company(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[JobDescription]:
        """Search job descriptions by company."""
        result = await self.session.execute(
            select(JobDescription)
            .where(JobDescription.company.ilike(f"%{query}%"))
            .order_by(desc(JobDescription.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_experience_level(
        self,
        experience_level: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[JobDescription]:
        """Get job descriptions by experience level."""
        return await self.get_by_filters(
            {"experience_level": experience_level},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )

    async def get_by_location(
        self,
        location: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[JobDescription]:
        """Get job descriptions by location."""
        result = await self.session.execute(
            select(JobDescription)
            .where(JobDescription.location.ilike(f"%{location}%"))
            .order_by(desc(JobDescription.created_at))
            .limit(limit)
            .offset(offset or 0)
        )
        return result.scalars().all()

    async def get_with_matches(self, job_id: int) -> Optional[JobDescription]:
        """Get job description with matches loaded."""
        result = await self.session.execute(
            select(JobDescription)
            .options(selectinload(JobDescription.job_matches))
            .where(JobDescription.id == job_id)
        )
        return result.scalar_one_or_none()

    async def get_recent_jobs(
        self,
        days: int = 30,
        limit: int = 50
    ) -> List[JobDescription]:
        """Get job descriptions created in the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        result = await self.session.execute(
            select(JobDescription)
            .where(JobDescription.created_at >= cutoff_date)
            .order_by(desc(JobDescription.created_at))
            .limit(limit)
        )
        return result.scalars().all()


class JobMatchRepository(BaseRepository[JobMatch]):
    """Repository for JobMatch entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(JobMatch, session)

    async def get_by_resume_id(
        self,
        resume_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[JobMatch]:
        """Get job matches for a specific resume."""
        return await self.get_by_filters(
            {"resume_id": resume_id},
            limit=limit,
            offset=offset,
            order_by="overall_match_score"
        )

    async def get_by_job_id(
        self,
        job_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[JobMatch]:
        """Get job matches for a specific job description."""
        return await self.get_by_filters(
            {"job_id": job_id},
            limit=limit,
            offset=offset,
            order_by="overall_match_score"
        )

    async def get_match(
        self,
        job_id: int,
        resume_id: int
    ) -> Optional[JobMatch]:
        """Get specific job-resume match."""
        result = await self.session.execute(
            select(JobMatch)
            .where(
                and_(
                    JobMatch.job_id == job_id,
                    JobMatch.resume_id == resume_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_top_matches(
        self,
        resume_id: int,
        min_score: float = 0.7,
        limit: int = 10
    ) -> List[JobMatch]:
        """Get top job matches for a resume above minimum score."""
        result = await self.session.execute(
            select(JobMatch)
            .where(
                and_(
                    JobMatch.resume_id == resume_id,
                    JobMatch.overall_match_score >= min_score
                )
            )
            .order_by(desc(JobMatch.overall_match_score))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_with_details(self, match_id: int) -> Optional[JobMatch]:
        """Get job match with job and resume details loaded."""
        result = await self.session.execute(
            select(JobMatch)
            .options(
                selectinload(JobMatch.job_description),
                selectinload(JobMatch.resume)
            )
            .where(JobMatch.id == match_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update_match(
        self,
        job_id: int,
        resume_id: int,
        **match_data
    ) -> JobMatch:
        """Create new match or update existing one."""
        existing_match = await self.get_match(job_id, resume_id)

        if existing_match:
            return await self.update(existing_match.id, **match_data)
        else:
            return await self.create(
                job_id=job_id,
                resume_id=resume_id,
                **match_data
            )

    async def get_matches_by_score_range(
        self,
        min_score: float,
        max_score: float,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[JobMatch]:
        """Get matches within a score range."""
        result = await self.session.execute(
            select(JobMatch)
            .where(
                and_(
                    JobMatch.overall_match_score >= min_score,
                    JobMatch.overall_match_score <= max_score
                )
            )
            .order_by(desc(JobMatch.overall_match_score))
            .limit(limit)
            .offset(offset or 0)
        )
        return result.scalars().all()
