"""Repository for books."""

from injector import Inject
from motor.motor_asyncio import AsyncIOMotorClient

from python_factory.example.entities.books import BookEntity
from python_factory.example.models.books.document import BookDocument


class BookRepository:
    """Repository for books."""

    def __init__(self, database: Inject[AsyncIOMotorClient]) -> None:  # type: ignore
        """Initialize BookRepository."""
        self.database: AsyncIOMotorClient = database  # type: ignore

    async def create(self, book_to_be_created: BookEntity) -> BookEntity:
        """Create a book."""
        document_to_be_created: BookDocument = BookDocument(**book_to_be_created.model_dump())
        async with await self.database.start_session() as session:
            document_created: BookDocument = await document_to_be_created.create(session=session)
        return BookEntity(**document_created.model_dump())
