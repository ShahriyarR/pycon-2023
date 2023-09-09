from typing import Any, List

from asyncpg.exceptions import UniqueViolationError
from esmerald import AsyncDAOProtocol
from saffier import ObjectNotFound

from blog.apps.accounts.models import User
from blog.apps.accounts.v1.schemas import UserOut


class UserDAO(AsyncDAOProtocol):
    model: User = User

    async def get_all(self, **kwargs: Any) -> List[Any]:
        """
        Gets all the users in the system.
        """
        user_list: List[User] = await self.model.query.all()
        return [
            UserOut(
                id=user.pk,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                username=user.username,
                is_superuser=user.is_superuser,
            )
            for user in user_list
        ]

    async def create(self, **kwargs: Any) -> Any:
        """Creates a user in the system"""
        try:
            await self.model.query.create_user(**kwargs)
        except UniqueViolationError as e:
            raise ValueError(str(e)) from e

    async def get(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Get the information of a user by ID.
        """
        try:
            user = await self.model.query.get(id=obj_id)
            return UserOut(**user.model_dump())
        except ObjectNotFound as e:
            raise ValueError(f"User with ID '{obj_id}' not found.") from e

    async def delete(self, obj_id: Any, **kwargs: Any) -> Any:
        """
        Deletes a user from the system by ID.
        """
        try:
            user = await self.model.query.get(id=obj_id)
            await user.delete()
        except ObjectNotFound as e:
            raise ValueError(f"User with ID '{obj_id}' not found.") from e
