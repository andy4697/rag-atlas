"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import create_app


@pytest.fixture
def app():
    """Create test FastAPI application."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)
