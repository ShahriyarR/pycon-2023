import saffier
from esmerald.conf import settings

_, registry = settings.db_access


class Article(saffier.Model):
    """
    Stores all the articles and related information
    about an article and a user.
    """

    user = saffier.ForeignKey("User", related_name="articles")
    title = saffier.CharField(max_length=255, null=False)
    content = saffier.TextField()
    created_at = saffier.DateTimeField(auto_now_add=True)
    updated_at = saffier.DateTimeField(auto_now=True)

    class Meta:
        registry = registry
