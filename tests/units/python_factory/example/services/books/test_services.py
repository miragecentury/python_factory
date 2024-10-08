"""Test the services module."""

from uuid import UUID

from python_factory.example.services.books.entities import BookEntity
from python_factory.example.services.books.enums import BookType
from python_factory.example.services.books.services import BookService
from python_factory.example.services.books.types import BookName


class TestBookService:
    """Test the BookService class."""

    def test_get_all_books(self) -> None:
        """Test get_all_books."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        assert len(books) >= 0

    def test_get_book(self) -> None:
        """Test get_book."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        for book in books:
            assert book == book_service.get_book(book_id=book.id)

    def test_add_book(self) -> None:
        """Test add_book."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book = BookEntity(title=BookName("Test Book"), book_type=BookType.FANTASY)
        book_service.add_book(book=book)

        assert book == book_service.get_book(book_id=book.id)
        assert book in book_service.get_all_books()
        assert len(book_service.get_all_books()) == len(books) + 1

    def test_add_book_already_exists(self) -> None:
        """Test add_book with a book that already exists."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book = books[0]

        try:
            book_service.add_book(book=book)
            assert False
        except ValueError as error:
            assert str(error) == f"Book with id {book.id} already exists."

        assert book in book_service.get_all_books()
        assert len(book_service.get_all_books()) == len(books)

    def test_remove_book(self) -> None:
        """Test remove_book."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book = books[0]
        book_service.remove_book(book_id=book.id)

        assert book not in book_service.get_all_books()
        assert len(book_service.get_all_books()) == len(books) - 1

    def test_remove_book_does_not_exist(self) -> None:
        """Test remove_book with a book that does not exist."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book_id = "00000000-0000-0000-0000-000000000000"

        try:
            book_service.remove_book(book_id=UUID(book_id))
            assert False
        except ValueError as error:
            assert str(error) == f"Book with id {book_id} does not exist."

        assert len(book_service.get_all_books()) == len(books)

    def test_update_book(self) -> None:
        """Test update_book."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book = books[0]
        book.title = BookName("Updated Title")
        book.book_type = BookType.FANTASY

        book_service.update_book(book=book)

        assert book == book_service.get_book(book_id=book.id)
        assert book in book_service.get_all_books()
        assert len(book_service.get_all_books()) == len(books)

    def test_update_book_does_not_exist(self) -> None:
        """Test update_book with a book that does not exist."""
        book_service = BookService()
        books: list[BookEntity] = book_service.get_all_books()

        book = BookEntity(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            title=BookName("Updated Title"),
            book_type=BookType.FANTASY,
        )

        try:
            book_service.update_book(book=book)
            assert False
        except ValueError as error:
            assert str(error) == f"Book with id {book.id} does not exist."

        assert len(book_service.get_all_books()) == len(books)
        assert len(book_service.get_all_books()) == len(books)
