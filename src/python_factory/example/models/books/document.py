"""Model for Book."""

from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed  # pyright: ignore[reportUnknownVariableType]
from pydantic import Field

from python_factory.example.entities.books import BookName, BookType


class BookDocument(Document):
    """BookModel."""

    id: Annotated[UUID, Indexed()] = Field(default_factory=uuid4)  # type: ignore
    name: Annotated[BookName, Indexed(unique=True)]
    type: Annotated[BookType, Indexed()]

    class Meta:
        """Meta class for BookModel."""

        collection: str = "books"
