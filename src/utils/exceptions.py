"""Custom exception classes."""

from typing import Any


class RAGSystemException(Exception):
    """Base exception for RAG system."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AgentException(RAGSystemException):
    """Exception raised by agents."""

    pass


class ServiceException(RAGSystemException):
    """Exception raised by services."""

    pass


class ConfigurationException(RAGSystemException):
    """Exception raised for configuration errors."""

    pass


class ValidationException(RAGSystemException):
    """Exception raised for validation errors."""

    pass


class ProcessingException(RAGSystemException):
    """Exception raised during data processing."""

    pass


class SearchException(RAGSystemException):
    """Exception raised during search operations."""

    pass


class EmbeddingException(RAGSystemException):
    """Exception raised during embedding operations."""

    pass
