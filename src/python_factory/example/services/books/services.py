"""Provides services for books."""

from typing import ClassVar
from uuid import UUID

from opentelemetry import metrics

from python_factory.core.plugins.opentelemetry_plugin.helpers import trace_span
from python_factory.example.services.books.types import BookName

from .entities import BookEntity
from .enums import BookType


class BookService:
    """Provides services for books."""

    book_store: ClassVar[dict[UUID, BookEntity]] = {}

    # Metrics Definitions
    METER_COUNTER_BOOK_ADD_NAME: str = "book_add"
    METER_COUNTER_BOOK_REMOVE_NAME: str = "book_remove"
    METER_COUNTER_BOOK_UPDATE_NAME: str = "book_update"
    # ====================

    def __init__(self, meter: metrics.Meter | None = None) -> None:
        """Initialize the service."""
        if meter is None:
            meter = metrics.get_meter(name=__name__)

        self._meter_counter_book_add: metrics.Counter = meter.create_counter(
            name=self.METER_COUNTER_BOOK_ADD_NAME,
            description="The number of books added.",
        )
        self._meter_counter_book_remove: metrics.Counter = meter.create_counter(
            name=self.METER_COUNTER_BOOK_REMOVE_NAME,
            description="The number of books removed.",
        )
        self._meter_counter_book_update = meter.create_counter(
            name=self.METER_COUNTER_BOOK_UPDATE_NAME,
            description="The number of books updated.",
        )

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

    @trace_span(name="Add Book")
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

        self._meter_counter_book_add.add(amount=1)

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

    @trace_span(name="Remove Book")
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

        self._meter_counter_book_remove.add(amount=1)

    @trace_span(name="Update Book")
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

        self._meter_counter_book_update.add(amount=1)
