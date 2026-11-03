
from abc import ABC, abstractmethod

from app.models.user import UsersDetails


class AuthRepositoryInterface(ABC):

    @abstractmethod
    async def get_user_by_username(
        self,
        username: str
    ) -> UsersDetails | None:
        pass

    @abstractmethod
    async def get_user_by_id(
        self,
        user_id: int
    ) -> UsersDetails | None:
        pass
