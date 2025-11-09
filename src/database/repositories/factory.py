"""Repository factory for creating repository instances."""

from sqlalchemy.ext.asyncio import AsyncSession

from .papers import PaperRepository, AuthorRepository, ChunkRepository
from .resumes import ResumeRepository, JobDescriptionRepository, JobMatchRepository


class RepositoryFactory:
    """Factory class for creating repository instances."""

    def __init__(self, session: AsyncSession):
        """Initialize factory with database session."""
        self.session = session

    @property
    def papers(self) -> PaperRepository:
        """Get paper repository."""
        return PaperRepository(self.session)

    @property
    def authors(self) -> AuthorRepository:
        """Get author repository."""
        return AuthorRepository(self.session)

    @property
    def chunks(self) -> ChunkRepository:
        """Get chunk repository."""
        return ChunkRepository(self.session)

    @property
    def resumes(self) -> ResumeRepository:
        """Get resume repository."""
        return ResumeRepository(self.session)

    @property
    def job_descriptions(self) -> JobDescriptionRepository:
        """Get job description repository."""
        return JobDescriptionRepository(self.session)

    @property
    def job_matches(self) -> JobMatchRepository:
        """Get job match repository."""
        return JobMatchRepository(self.session)


def get_repositories(session: AsyncSession) -> RepositoryFactory:
    """Get repository factory instance."""
    return RepositoryFactory(session)
