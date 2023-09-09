from blog.apps.accounts.models import User as UserModel
from blog.apps.articles.models import Article as ArticleModel
from esmerald_admin import Admin, ModelView
from blog.apps.posts.models import Post as PostModel

User = UserModel.declarative()
Article = ArticleModel.declarative()
Post = PostModel.declarative()


class UserAdmin(ModelView, model=User):
    icon = "fa-solid fa-table"
    column_list = [User.id, User.username, User.email, User.first_name, User.last_name]


class ArticleAdmin(ModelView, model=Article):
    icon = "fa-solid fa-table"
    column_list = [
        Article.id,
        Article.user,
        Article.created_at,
        Article.updated_at,
    ]
    form_ajax_refs = {
        "user_relation": {
            "fields": ("email", "username"),
            "order_by": ("id",),
        }
    }


class PostAdmin(ModelView, model=Post):
    icon = "fa-solid fa-table"
    column_list = [Post.id, Post.content, Post.updated_at]
    form_ajax_refs = {
        "user_relation": {
            "fields": ("email", "username"),
            "order_by": ("id",),
        },
        "article_relation": {
            "fields": ["content"],
            "order_by": ("id",),
        },
    }


def get_views(admin: Admin) -> None:
    """Generates the admin views"""
    admin.add_model_view(UserAdmin)
    admin.add_model_view(ArticleAdmin)
    admin.add_model_view(PostAdmin)
