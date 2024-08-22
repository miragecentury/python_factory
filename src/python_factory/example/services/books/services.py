"""Provides services for books."""

from typing import ClassVar
from uuid import UUID

from python_factory.example.services.books.types import BookName

from .entities import BookEntity
from .enums import BookType


class BookService:
    """Provides services for books."""

    book_store: ClassVar[dict[UUID, BookEntity]] = {}

    def __init__(self) -> None:
        """Initialize the service."""
        # Build the book store if it is empty
        if len(self.book_store) == 0:
            self.build_book_store()

    @classmethod
    def build_book_store(cls) -> None:
        """Build the book store."""
        books: list[BookEntity] = [
            BookEntity(title=BookName("Book 1"), book_type=BookType.FANTASY),
            BookEntity(title=BookName("Book 2"), book_type=BookType.MYSTERY),
            BookEntity(title=BookName("Book 3"), book_type=BookType.SCIENCE_FICTION),
        ]

        cls.book_store = {book.id: book for book in books}

    def get_all_books(self) -> list[BookEntity]:
        """Get all books.

        Returns:
            list[BookEntity]: All books
        """
        return list(self.book_store.values())
