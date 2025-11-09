"""Common utility functions."""

import asyncio
import hashlib
import uuid
from datetime import datetime
from functools import wraps
from typing import Any


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def generate_hash(content: str) -> str:
    """Generate SHA-256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary."""
    return data.get(key, default)


def chunk_list(items: list[Any], chunk_size: int) -> list[list[Any]]:
    """Split list into chunks of specified size."""
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def retry_async(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying async functions."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2**attempt))
                    continue
            raise last_exception

        return wrapper

    return decorator


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    import re

    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(" .")
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        filename = name[: 255 - len(ext) - 1] + "." + ext if ext else name[:255]
    return filename


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"
