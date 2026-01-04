from abc import ABC, abstractmethod
from entitis.user import User


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User)-> User:
        pass

    @abstractmethod
    def get_user_by_email(self, useremail: str)-> User | None:
        pass
