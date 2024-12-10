"""Repository for books."""

from typing import Any
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from pymongo.results import DeleteResult

from python_factory.example.entities.books import BookEntity
from python_factory.example.models.books.document import BookDocument


class BookRepository:
    """Repository for books."""

    def __init__(self, client: AsyncIOMotorClient) -> None:  # type: ignore
        """Initialize BookRepository."""
        self.client: AsyncIOMotorClient[Any] = client

    async def create(
        self, book_to_be_created: BookEntity, session: AsyncIOMotorClientSession | None = None
    ) -> BookEntity:
        """Create a book."""
        # If session is None, create a standalone session and call the method again.
        if session is None:
            async with await self.client.start_session() as standalone_session:
                return await self.create(book_to_be_created=book_to_be_created, session=standalone_session)

        document_to_be_created: BookDocument = BookDocument(**book_to_be_created.model_dump())
        async with await self.client.start_session() as standalone_session:
            document_created: BookDocument = await document_to_be_created.create(session=standalone_session)
        return BookEntity(**document_created.model_dump())

    async def get_one_by_id(
        self, document_id: UUID, session: AsyncIOMotorClientSession | None = None
    ) -> BookEntity | None:
        """Get a book by id."""
        # If session is None, create a standalone session and call the method again.
        if session is None:
            async with await self.client.start_session() as standalone_session:
                return await self.get_one_by_id(document_id=document_id, session=standalone_session)

        find_one: BookDocument | None = await BookDocument.find_one(  # type: ignore
            BookDocument.id == document_id, session=session
        )

        if find_one is None:
            return None

        return BookEntity(**find_one.model_dump())

    async def delete_one_by_id(self, document_id: UUID, session: AsyncIOMotorClientSession | None = None) -> None:
        """Delete a book by id."""
        # If session is None, create a standalone session and call the method again.
        if session is None:
            async with await self.client.start_session() as standalone_session:
                return await self.delete_one_by_id(document_id=document_id, session=standalone_session)

        book_document_to_delete: BookDocument | None = await BookDocument.find_one(  # pyright: ignore
            BookDocument.id == document_id, session=session
        )
        if book_document_to_delete is None:
            return

        result: DeleteResult | None = await BookDocument.delete(  # pyright: ignore
            book_document_to_delete, session=session
        )

        if result is None:
            return

        if result.deleted_count == 1 and result.acknowledged:
            return

        raise Exception("Failed to delete book.")
