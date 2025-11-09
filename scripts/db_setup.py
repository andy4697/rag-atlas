#!/usr/bin/env python3
"""Database setup and management script."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database.init_db import init_db, drop_db, create_database_if_not_exists
from src.core.config import get_settings


async def main():
    """Main CLI function."""
    if len(sys.argv) < 2:
        print("Usage: python db_setup.py [init|drop|create]")
        print("  init   - Initialize database with tables")
        print("  drop   - Drop all tables")
        print("  create - Create database if it doesn't exist")
        sys.exit(1)
    
    command = sys.argv[1]
    settings = get_settings()
    
    try:
        if command == "init":
            print("Initializing database...")
            await init_db()
            print("Database initialization complete!")
            
        elif command == "drop":
            print("Dropping all tables...")
            await drop_db()
            print("All tables dropped!")
            
        elif command == "create":
            print("Creating database if it doesn't exist...")
            database_name = settings.database_url.split("/")[-1]
            await create_database_if_not_exists(settings.database_url, database_name)
            print("Database creation complete!")
            
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())