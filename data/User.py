import typing

import components.core


class User:
    """Data class that stores user data."""
    name: str
    faculty: str
    need: typing.List[str]
    give: typing.List[str]
    user_hash: int

    def __init__(self, name: str, faculty: str, need: typing.List[str], give: typing.List[str]):
        self.name = name
        self.faculty = faculty
        self.need = need
        self.give = give
        user_hash = components.core.generate_hash()

    def to_dict(self):
        return {
            "name": self.name,
            "faculty": self.faculty,
            "need": self.need,
            "give": self.give
        }
