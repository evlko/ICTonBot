import typing

import components.core


def __init_():
    self = User("", "", [], [])


class User:
    """Data class that stores user data."""
    name: str
    faculty: str
    need_subjects: typing.List[str]
    give_subjects: typing.List[str]
    user_hash: int

    def __init__(self, name: str, faculty: str, need: typing.List[str], give: typing.List[str]):
        """A class constructor that automatically generates user hash."""

        self.name = name
        self.faculty = faculty
        self.need_subjects = need
        self.give_subjects = give
        user_hash = components.core.generate_hash()

    def to_dict(self) -> typing.Dict:
        """A method that is used for user data serialization to dictionary."""

        return {
            "name": self.name,
            "faculty": self.faculty,
            "need": self.need_subjects,
            "give": self.give_subjects,
            "hash": self.user_hash
        }


class UserFactory:
    @staticmethod
    def fake_user() -> User:
        return User("", "", [], [])
