import saffier
from esmerald.conf import settings

_, registry = settings.db_access


class Post(saffier.Model):
    """
    Stores all the posts for a given article and user
    """

    user = saffier.ForeignKey("User", related_name="posts")
    article = saffier.ForeignKey("Article", related_name="posts")
    content = saffier.CharField(max_length=500)
    created_at = saffier.DateTimeField(auto_now_add=True)
    updated_at = saffier.DateTimeField(auto_now=True)

    class Meta:
        registry = registry
