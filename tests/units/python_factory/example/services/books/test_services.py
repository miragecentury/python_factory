"""Test the services module."""

from python_factory.example.services.books.entities import BookEntity
from python_factory.example.services.books.services import BookService


class TestBookService:
    """Test the BookService class."""

    def test_get_all_books(self) -> None:
        """Test get_all_books."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        assert len(books) >= 0
