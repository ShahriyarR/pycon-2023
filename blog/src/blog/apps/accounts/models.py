from esmerald.conf import settings
from esmerald.contrib.auth.saffier.base_user import AbstractUser

_, registry = settings.db_access


class User(AbstractUser):
    """
    Base for all the users of the system.
    """

    class Meta:
        registry = registry
