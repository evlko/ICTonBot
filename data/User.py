import typing

import components.core


def __init_():
    self = User("", "", [], [], 0)


class User:
    """Data class that stores user data."""
    name: str
    faculty: str
    need_subjects: typing.List[str]
    give_subjects: typing.List[str]
    id: int

    def __init__(self, name: str, faculty: str, need: typing.List[str], give: typing.List[str], id: int):
        """A class constructor that automatically generates user hash."""

        self.name = name
        self.faculty = faculty
        self.need_subjects = need
        self.give_subjects = give

    def to_dict(self) -> typing.Dict:
        """A method that is used for user data serialization to dictionary."""

        return {
            "name": self.name,
            "faculty": self.faculty,
            "need": self.need_subjects,
            "give": self.give_subjects,
            "id": self.id
        }


class UserFactory:
    @staticmethod
    def new_fake_user() -> User:
        return User("", "", [], [], 0)
