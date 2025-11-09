"""Repository classes for paper-related entities."""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Paper, Author, Chunk, PaperAuthor, Category, PaperCategory
from .base import BaseRepository


class PaperRepository(BaseRepository[Paper]):
    """Repository for Paper entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(Paper, session)

    async def get_by_arxiv_id(self, arxiv_id: str) -> Optional[Paper]:
        """Get paper by arXiv ID."""
        return await self.get_by_field("arxiv_id", arxiv_id)
    async def get_with_authors(self, paper_id: int) -> Optional[Paper]:
        """Get paper with authors loaded."""
        result = await self.session.execute(
            select(Paper)
            .options(
                selectinload(Paper.paper_authors).selectinload(PaperAuthor.author)
            )
            .where(Paper.id == paper_id)
        )
        return result.scalar_one_or_none()

    async def get_with_chunks(self, paper_id: int) -> Optional[Paper]:
        """Get paper with chunks loaded."""
        result = await self.session.execute(
            select(Paper)
            .options(selectinload(Paper.chunks))
            .where(Paper.id == paper_id)
        )
        return result.scalar_one_or_none()

    async def search_by_title(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Paper]:
        """Search papers by title using full-text search."""
        result = await self.session.execute(
            select(Paper)
            .where(Paper.title.ilike(f"%{query}%"))
            .order_by(desc(Paper.published_date))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def search_by_abstract(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Paper]:
        """Search papers by abstract content."""
        result = await self.session.execute(
            select(Paper)
            .where(Paper.abstract.ilike(f"%{query}%"))
            .order_by(desc(Paper.published_date))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Paper]:
        """Get papers published within date range."""
        query = (
            select(Paper)
            .where(
                and_(
                    Paper.published_date >= start_date,
                    Paper.published_date <= end_date
                )
            )
            .order_by(desc(Paper.published_date))
        )

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_categories(
        self,
        category_codes: List[str],
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Paper]:
        """Get papers by category codes."""
        query = (
            select(Paper)
            .join(PaperCategory)
            .join(Category)
            .where(Category.code.in_(category_codes))
            .order_by(desc(Paper.published_date))
        )

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_status(
        self,
        status: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Paper]:
        """Get papers by processing status."""
        return await self.get_by_filters(
            {"status": status},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )

    async def get_recent_papers(self, days: int = 7, limit: int = 50) -> List[Paper]:
        """Get papers published in the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return await self.get_by_date_range(
            start_date=cutoff_date,
            end_date=datetime.utcnow(),
            limit=limit
        )

    async def update_processing_status(
        self,
        paper_id: int,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Paper]:
        """Update paper processing status and metadata."""
        update_data = {"status": status}
        if metadata:
            update_data["processing_metadata"] = metadata

        return await self.update(paper_id, **update_data)


class AuthorRepository(BaseRepository[Author]):
    """Repository for Author entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(Author, session)

    async def get_by_name(self, name: str) -> Optional[Author]:
        """Get author by name."""
        return await self.get_by_field("name", name)

    async def get_by_orcid(self, orcid: str) -> Optional[Author]:
        """Get author by ORCID."""
        return await self.get_by_field("orcid", orcid)

    async def search_by_name(self, query: str, limit: int = 10) -> List[Author]:
        """Search authors by name."""
        result = await self.session.execute(
            select(Author)
            .where(Author.name.ilike(f"%{query}%"))
            .order_by(Author.name)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_with_papers(self, author_id: int) -> Optional[Author]:
        """Get author with papers loaded."""
        result = await self.session.execute(
            select(Author)
            .options(
                selectinload(Author.paper_authors).selectinload(PaperAuthor.paper)
            )
            .where(Author.id == author_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(self, name: str, **kwargs) -> Author:
        """Get existing author or create new one."""
        author = await self.get_by_name(name)
        if author:
            return author

        return await self.create(name=name, **kwargs)


class ChunkRepository(BaseRepository[Chunk]):
    """Repository for Chunk entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(Chunk, session)

    async def get_by_paper_id(
        self,
        paper_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Chunk]:
        """Get chunks for a specific paper."""
        return await self.get_by_filters(
            {"paper_id": paper_id},
            limit=limit,
            offset=offset,
            order_by="chunk_index"
        )

    async def get_by_section_type(
        self,
        section_type: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Chunk]:
        """Get chunks by section type."""
        return await self.get_by_filters(
            {"section_type": section_type},
            limit=limit,
            offset=offset,
            order_by="created_at"
        )

    async def search_content(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Chunk]:
        """Search chunks by content."""
        result = await self.session.execute(
            select(Chunk)
            .where(Chunk.content.ilike(f"%{query}%"))
            .order_by(desc(Chunk.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_chunks_with_embeddings(
        self,
        embedding_model: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Chunk]:
        """Get chunks that have embeddings."""
        filters = {}
        if embedding_model:
            filters["embedding_model"] = embedding_model

        result = await self.session.execute(
            select(Chunk)
            .where(
                and_(
                    Chunk.embedding.isnot(None),
                    *[getattr(Chunk, k) == v for k, v in filters.items()]
                )
            )
            .order_by(Chunk.created_at)
            .limit(limit)
            .offset(offset or 0)
        )
        return result.scalars().all()

    async def update_embedding(
        self,
        chunk_id: int,
        embedding: List[float],
        model: str
    ) -> Optional[Chunk]:
        """Update chunk embedding."""
        return await self.update(
            chunk_id,
            embedding=embedding,
            embedding_model=model
        )

    async def bulk_update_embeddings(
        self,
        chunk_embeddings: List[Dict[str, Any]]
    ) -> None:
        """Bulk update embeddings for multiple chunks."""
        for item in chunk_embeddings:
            await self.update(
                item["chunk_id"],
                embedding=item["embedding"],
                embedding_model=item["model"]
            )

    async def get_similar_chunks(
        self,
        embedding: List[float],  # pylint: disable=unused-argument
        limit: int = 10,
        threshold: float = 0.7  # pylint: disable=unused-argument
    ) -> List[Chunk]:
        """Get similar chunks using vector similarity (placeholder for vector DB)."""
        # This is a placeholder - in production you'd use a proper vector database
        # like FAISS, Chroma, or PostgreSQL with pgvector extension

        # For now, return chunks with embeddings
        return await self.get_chunks_with_embeddings(limit=limit)

    async def delete_by_paper_id(self, paper_id: int) -> int:
        """Delete all chunks for a paper."""
        return await self.delete_by_filters({"paper_id": paper_id})
