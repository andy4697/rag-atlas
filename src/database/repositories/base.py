"""Base repository class with common CRUD operations."""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import and_, delete, select, update
from sqlalchemy.sql.functions import count
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    """Base repository class with common CRUD operations."""

    def __init__(self, model: Type[Model], session: AsyncSession):
        """Initialize repository with model and session."""
        self.model = model
        self.session = session

    async def create(self, **kwargs) -> Model:
        """Create a new record."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, record_id: int) -> Optional[Model]:
        """Get record by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == record_id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any) -> Optional[Model]:
        """Get record by specific field."""
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, field) == value)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Model]:
        """Get all records with optional pagination and ordering."""
        query = select(self.model)

        if order_by:
            if hasattr(self.model, order_by):
                query = query.order_by(getattr(self.model, order_by))

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_filters(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None
    ) -> List[Model]:
        """Get records by multiple filters."""
        query = select(self.model)

        # Apply filters
        conditions = []
        for field, value in filters.items():
            if hasattr(self.model, field):
                if isinstance(value, list):
                    conditions.append(getattr(self.model, field).in_(value))
                else:
                    conditions.append(getattr(self.model, field) == value)

        if conditions:
            query = query.where(and_(*conditions))

        # Apply ordering
        if order_by:
            if hasattr(self.model, order_by):
                query = query.order_by(getattr(self.model, order_by))

        # Apply pagination
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, record_id: int, **kwargs) -> Optional[Model]:
        """Update record by ID."""
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_by_id(record_id)

        await self.session.execute(
            update(self.model)
            .where(self.model.id == record_id)
            .values(**update_data)
        )

        return await self.get_by_id(record_id)

    async def delete(self, record_id: int) -> bool:
        """Delete record by ID."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == record_id)
        )
        return result.rowcount > 0

    async def delete_by_filters(self, filters: Dict[str, Any]) -> int:
        """Delete records by filters. Returns count of deleted records."""
        conditions = []
        for field, value in filters.items():
            if hasattr(self.model, field):
                if isinstance(value, list):
                    conditions.append(getattr(self.model, field).in_(value))
                else:
                    conditions.append(getattr(self.model, field) == value)

        if not conditions:
            return 0

        result = await self.session.execute(
            delete(self.model).where(and_(*conditions))
        )
        return result.rowcount

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters."""
        query = select(count(self.model.id))

        if filters:
            conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field):
                    if isinstance(value, list):
                        conditions.append(getattr(self.model, field).in_(value))
                    else:
                        conditions.append(getattr(self.model, field) == value)

            if conditions:
                query = query.where(and_(*conditions))

        result = await self.session.execute(query)
        return result.scalar()

    async def exists(self, **kwargs) -> bool:
        """Check if record exists with given criteria."""
        conditions = []
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                conditions.append(getattr(self.model, field) == value)

        if not conditions:
            return False

        query = select(count(self.model.id)).where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalar() > 0

    async def bulk_create(self, objects: List[Dict[str, Any]]) -> List[Model]:
        """Create multiple records in bulk."""
        instances = [self.model(**obj) for obj in objects]
        self.session.add_all(instances)
        await self.session.flush()

        # Refresh all instances to get IDs
        for instance in instances:
            await self.session.refresh(instance)

        return instances

    async def get_with_relations(
        self,
        record_id: int,
        relations: List[str]
    ) -> Optional[Model]:
        """Get record by ID with specified relations loaded."""
        query = select(self.model).where(self.model.id == record_id)

        # Add selectinload for each relation
        for relation in relations:
            if hasattr(self.model, relation):
                query = query.options(selectinload(getattr(self.model, relation)))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
