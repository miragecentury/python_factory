"""Provides the response objects for the books API."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from python_factory.example.entities.books import BookName, BookType


class BookResponseModel(BaseModel):
    """Book response model."""

    model_config = ConfigDict(extra="ignore")

    id: UUID
    title: BookName
    book_type: BookType


class BookListReponse(BaseModel):
    """Book list response."""

    model_config = ConfigDict(extra="forbid")

    books: list[BookResponseModel]
    size: int
