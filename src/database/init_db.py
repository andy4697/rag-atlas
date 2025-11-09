"""Database initialization utilities."""

import asyncio
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import get_settings
from src.database.models import Base


async def create_database_if_not_exists(database_url: str, database_name: str) -> None:
    """Create database if it doesn't exist."""
    # Connect to postgres database to create our target database
    postgres_url = database_url.replace(f"/{database_name}", "/postgres")
    engine = create_async_engine(postgres_url, isolation_level="AUTOCOMMIT")
    
    async with engine.connect() as conn:
        # Check if database exists
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
            {"db_name": database_name}
        )
        
        if not result.fetchone():
            # Create database
            await conn.execute(text(f'CREATE DATABASE "{database_name}"'))
            print(f"Created database: {database_name}")
        else:
            print(f"Database {database_name} already exists")
    
    await engine.dispose()


async def init_db(database_url: Optional[str] = None) -> None:
    """Initialize database with tables."""
    if database_url is None:
        settings = get_settings()
        database_url = settings.database_url
    
    # Extract database name from URL
    database_name = database_url.split("/")[-1]
    
    # Create database if it doesn't exist
    await create_database_if_not_exists(database_url, database_name)
    
    # Create tables
    engine = create_async_engine(database_url)
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("Created all database tables")
    
    await engine.dispose()


async def drop_db(database_url: Optional[str] = None) -> None:
    """Drop all database tables."""
    if database_url is None:
        settings = get_settings()
        database_url = settings.database_url
    
    engine = create_async_engine(database_url)
    
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        print("Dropped all database tables")
    
    await engine.dispose()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        asyncio.run(drop_db())
    else:
        asyncio.run(init_db())