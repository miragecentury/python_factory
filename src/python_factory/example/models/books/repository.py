"""Repository for books."""

from python_factory.core.plugins.odm_plugin.repositories import AbstractRepository
from python_factory.example.entities.books import BookEntity
from python_factory.example.models.books.document import BookDocument


class BookRepository(AbstractRepository[BookDocument, BookEntity]):
    """Repository for books."""
