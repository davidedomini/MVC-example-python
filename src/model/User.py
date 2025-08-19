from dataclasses import dataclass
from typing import List, Callable

@dataclass
class User:
    username: str
    email: str
    birthdate: str
    password: str
    
class UserModel:
    def __init__(self):
        self._users: List[User] = []
        self._observers: List[Callable[["UserModel"], None]] = []

    # Observer API
    def add_observer(self, callback: Callable[["UserModel"], None]):
        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback: Callable[["UserModel"], None]):
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify(self):
        for cb in list(self._observers):
            cb(self)

    # Update model 
    def register_user(self, user: User):
        self._users.append(user)
        self._notify()

    # Query
    @property
    def count(self) -> int:
        return len(self._users)

    @property
    def users(self) -> List[User]:
        return list(self._users) 
