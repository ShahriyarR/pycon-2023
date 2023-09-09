from typing import Any, List

from esmerald import AsyncDAOProtocol
from saffier import ObjectNotFound

from blog.apps.accounts.v1.daos import UserDAO
from blog.apps.articles.models import Article
from blog.apps.articles.v1.daos import ArticleDAO
from blog.apps.posts.models import Post
from blog.apps.posts.v1.schemas import PostOut


class PostDAO(AsyncDAOProtocol):
    model: Post = Post

    async def get(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Gets the post record from the database directly.
        """
        try:
            return await self.model.query.get(pk=obj_id)
        except ObjectNotFound as e:
            raise ValueError(f"Post '{obj_id}' not found.") from e

    async def get_all(self, **kwargs: Any) -> List[PostOut]:
        article_id = kwargs.get("article_id")
        article_dao = ArticleDAO()

        article = await article_dao.get(article_id)

        posts: List[Post] = await self.model.query.filter(article__id=article.id)
        posts_out: List[PostOut] = []

        for post in posts:
            await post.user.load()
            posts_out.append(
                PostOut(
                    id=post.pk,
                    content=post.content,
                    user=post.user.username,
                    created_at=str(post.created_at),
                )
            )
        return posts_out

    async def create(self, **kwargs: Any) -> Any:
        """
        Creates a post for a user associated to a specific article.
        """
        article_id = kwargs.pop("article_id")
        article_dao = ArticleDAO()

        # Validates if exists
        await article_dao.get(article_id)
        article = Article(id=article_id)

        user = kwargs.pop("user")
        user_dao = UserDAO()
        await user.load()

        # Validates if exists
        await user_dao.get(obj_id=user)

        post: Post = await self.model.query.create(user=user, article=article, **kwargs)

        return PostOut(
            id=post.pk,
            content=post.content,
            created_at=str(post.created_at),
            user=user.username,
        )

    async def delete(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Deletes a post from a specific article.
        """
        article_id = kwargs.pop("article_id")
        article_dao = ArticleDAO()

        # Validates if exists
        await article_dao.get(article_id)

        # Validates if exists
        await self.get(obj_id=obj_id)

        post = await self.model.query.get(id=obj_id)
        await post.delete()
