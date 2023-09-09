"""
Generated by 'esmerald createapp' using Esmerald 2.0.5.
"""
from typing import List

from esmerald import delete, get, post, put
from esmerald.openapi.datastructures import OpenAPIResponse

from .daos import ArticleDAO
from .schemas import ArticleIn, ArticleOut, ArticleUpdate, Error


@get(
    "/articles",
    tags=["Article"],
    description="List of all the articles in the system",
    summary="Lists all articles",
    responses={
        200: OpenAPIResponse(model=[ArticleOut]),
        400: OpenAPIResponse(model=Error, description="Bad response"),
    },
)
async def articles() -> List[ArticleOut]:
    """
    Lists all the articles.
    """
    article_dao = ArticleDAO()
    return await article_dao.get_all()


@get(
    "/{id}",
    tags=["Article"],
    summary="Get a article",
    description="Shows the information of a user",
    responses={
        200: OpenAPIResponse(model=ArticleOut),
        400: OpenAPIResponse(model=Error, description="Bad response"),
    },
)
async def article(id: int) -> ArticleOut:
    """
    Gets an article by ID
    """
    article = ArticleDAO()
    return await article.get(obj_id=id)


@post(
    "/create",
    tags=["Article"],
    summary="Create an article",
    description="Creates a user in the system",
    responses={400: OpenAPIResponse(model=Error, description="Bad response")},
)
async def create_article(data: ArticleIn) -> None:
    """
    Creates an article for a user
    """
    article = ArticleDAO()
    await article.create(**data.model_dump())


@delete(
    "/{user}/{id}",
    summary="Delete an article",
    tags=["Article"],
    description="Deletes an article from the system by ID",
    responses={
        400: OpenAPIResponse(model=Error, description="Bad response"),
    },
)
async def delete_article(id: int, user: int) -> None:
    """
    Deletes an article by user id.
    """
    article = ArticleDAO()
    await article.delete(obj_id=id, user=user)


@put(
    "/{user}/{id}",
    summary="Update an article",
    tags=["Article"],
    description="Updates a user article by ID",
    responses={
        200: OpenAPIResponse(model=ArticleOut, description="The article"),
        400: OpenAPIResponse(model=Error, description="Bad response"),
    },
)
async def update_article(data: ArticleUpdate, user: int, id: int) -> ArticleOut:
    """
    Updates an article for a user by ID
    """
    article = ArticleDAO()
    return await article.update(
        obj_id=id, user=user, **data.model_dump(exclude_none=True)
    )
