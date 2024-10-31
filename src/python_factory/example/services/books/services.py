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
    def build_default_book_store(cls) -> list[BookEntity]:
        """Build the default book store."""
        return [
            BookEntity(title=BookName("Book 1"), book_type=BookType.FANTASY),
            BookEntity(title=BookName("Book 2"), book_type=BookType.MYSTERY),
            BookEntity(title=BookName("Book 3"), book_type=BookType.SCIENCE_FICTION),
        ]

    @classmethod
    def build_book_store(cls, books: list[BookEntity] | None = None) -> None:
        """Build the book store.

        Args:
            books (list[BookEntity], optional): The books to add. Defaults to None.
        """
        if books is None:
            books = cls.build_default_book_store()

        cls.book_store = {book.id: book for book in books}

    def add_book(self, book: BookEntity) -> None:
        """Add a book.

        Args:
            book (BookEntity): The book to add

        Raises:
            ValueError: If the book already exists.
        """
        if book.id in self.book_store:
            raise ValueError(f"Book with id {book.id} already exists.")

        self.book_store[book.id] = book

    def get_book(self, book_id: UUID) -> BookEntity:
        """Get a book.

        Args:
            book_id (UUID): The book id

        Returns:
            BookEntity: The book

        Raises:
            ValueError: If the book does not exist.
        """
        if book_id not in self.book_store:
            raise ValueError(f"Book with id {book_id} does not exist.")

        return self.book_store[book_id]

    def get_all_books(self) -> list[BookEntity]:
        """Get all books.

        Returns:
            list[BookEntity]: All books
        """
        return list(self.book_store.values())

    def remove_book(self, book_id: UUID) -> None:
        """Remove a book.

        Args:
            book_id (UUID): The book id

        Raises:
            ValueError: If the book does not exist.
        """
        if book_id not in self.book_store:
            raise ValueError(f"Book with id {book_id} does not exist.")

        del self.book_store[book_id]

    def update_book(self, book: BookEntity) -> None:
        """Update a book.

        Args:
            book (BookEntity): The book to update

        Raises:
            ValueError: If the book does not exist.
        """
        if book.id not in self.book_store:
            raise ValueError(f"Book with id {book.id} does not exist.")

        self.book_store[book.id] = book
