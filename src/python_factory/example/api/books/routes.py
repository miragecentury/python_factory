"""Provides the Books API."""

from typing import cast

import injector
from fastapi import APIRouter

from python_factory.core.utils.injector_fastapi import inject_depends
from python_factory.example.services.books import BookEntity, BookService

from .responses import BookListReponse, BookResponseModel

api_v1_books_router: APIRouter = APIRouter(prefix="/books")
api_v2_books_router: APIRouter = APIRouter(prefix="/books")


@api_v1_books_router.get(path="", response_model=BookListReponse)
@injector.inject
def get_books(
    books_service: BookService = inject_depends(BookService),
) -> BookListReponse:
    """Get all books.

    Args:
        books_service (BookService): Book service.

    Returns:
        BookListReponse: List of books
    """
    books: list[BookEntity] = books_service.get_all_books()

    return BookListReponse(
        books=cast(
            list[BookResponseModel],
            map(lambda book: BookResponseModel(**book.model_dump()), books),
        ),
        size=len(books),
    )
