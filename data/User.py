import json
import typing

from components.config import UserState


class User:
    """Data class that stores user data."""
    name: str
    faculty: str
    need_subjects: typing.List[str]
    give_subjects: typing.List[str]
    state: str
    username: str

    def __init__(self, name: str, faculty: str, need: typing.List[str], give: typing.List[str], state: str,
                 username: str):
        """A class constructor that automatically generates user hash."""

        self.name = name
        self.faculty = faculty
        self.need_subjects = need
        self.give_subjects = give
        self.state = state
        self.username = username

    def to_dict(self) -> typing.Dict:
        """A method that is used for user data serialization to dictionary."""

        return {
            "name": self.name,
            "faculty": self.faculty,
            "need": self.need_subjects,
            "give": self.give_subjects,
            "state": self.state,
            "username": self.username
        }


class UserFactory:
    @staticmethod
    def new_fake_user() -> User:
        return User("", "", [], [], UserState.START.value[0], "")

    @staticmethod
    def new_user(name: str, faculty: str, need_subjects: typing.List[str], give_subjects: typing.List[str],
                 state: str, username: str) -> User:
        return User(name=name, faculty=faculty, need=need_subjects, give=give_subjects, state=state, username=username)

    @staticmethod
    def from_dict(data: dict) -> User:
        return UserFactory.new_user(data["name"], data["faculty"], data["need"], data["give"], data["state"],
                                    data["username"])


def serialized(user: User) -> str:
    return json.dumps(user.to_dict())


def deserialized(data) -> User:
    return UserFactory.from_dict(json.loads(data))
