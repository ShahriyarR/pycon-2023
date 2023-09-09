from typing import Any, List

from asyncpg.exceptions import ForeignKeyViolationError
from esmerald import AsyncDAOProtocol
from saffier import ObjectNotFound

from blog.apps.accounts.v1.daos import UserDAO
from blog.apps.articles.models import Article
from blog.apps.articles.v1.schemas import ArticleOut


class ArticleDAO(AsyncDAOProtocol):
    model: Article = Article

    async def get_all(self, **kwargs: Any) -> List[Any]:
        """
        All the articles in the system.
        """
        articles: List[Article] = await self.model.query.all()
        return [
            ArticleOut(
                id=article.id,
                user=article.user.pk,
                title=article.title,
                content=article.content,
                created_at=str(article.created_at),
                updated_at=str(article.updated_at),
            )
            for article in articles
        ]

    async def get(self, obj_id: Any, **kwargs: Any) -> Any:
        try:
            article: Article = await self.model.query.get(id=obj_id)
            return ArticleOut(
                id=article.pk,
                user=article.user.pk,
                title=article.title,
                content=article.content,
                created_at=str(article.created_at),
                updated_at=str(article.updated_at),
            )
        except ObjectNotFound as e:
            raise ValueError(f"Article with ID '{obj_id}' not found.") from e

    async def create(self, **kwargs: Any) -> Any:
        """
        Creates articles for a specific user
        """
        user = kwargs.get("user")
        try:
            return await self.model.query.create(**kwargs)
        except ObjectNotFound as e:
            raise ValueError(str(e)) from e
        except ForeignKeyViolationError as e:
            raise ValueError(f"User with ID '{user.pk}' not found.") from e

    async def delete(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Deletes an article by user.

        Reuses the existing UserDAO to manipulate the user objects.
        """
        user_dao = UserDAO()
        user_id = kwargs.get("user")

        user = await user_dao.get(user_id)

        try:
            article = await self.model.query.get(id=obj_id, user__id=user.id)
            await article.delete()
        except ObjectNotFound as e:
            raise ValueError(
                f"Article with ID '{obj_id}' for the user '{user_id}' was not found."
            ) from e

    async def update(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Updates the article for a specific user
        """
        user_dao = UserDAO()
        user_id = kwargs.pop("user")

        user = await user_dao.get(user_id)

        try:
            article = await self.model.query.get(id=obj_id, user__id=user.id)
            await article.update(**kwargs)

            article = await self.model.query.get(id=obj_id, user__id=user.id)
            return ArticleOut(
                id=article.pk,
                user=article.user.pk,
                title=article.title,
                content=article.content,
                created_at=str(article.created_at),
                updated_at=str(article.updated_at),
            )
        except ObjectNotFound as e:
            raise ValueError(
                f"Article with ID '{obj_id}' for the user '{user_id}' was not found."
            ) from e
