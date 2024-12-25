"""Model for Book."""

from typing import Annotated

from beanie import Indexed  # pyright: ignore[reportUnknownVariableType]

from python_factory.core.plugins.odm_plugin.documents import BaseDocument
from python_factory.example.entities.books import BookName, BookType


class BookDocument(BaseDocument):
    """BookModel."""

    title: Annotated[BookName, Indexed(unique=True)]
    book_type: Annotated[BookType, Indexed()]

    class Settings(BaseDocument.Settings):
        """Meta class for BookModel."""

        collection: str = "books"
