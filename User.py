import typing


class User:
    """Data class that stores user data."""
    name: str
    faculty: str
    need: typing.List[str]
    give: typing.List[str]

    def __init__(self, name: str, faculty: str, need: typing.List[str], give: typing.List[str]):
        self.name = name
        self.faculty = faculty
        self.need = need
        self.give = give

    def to_dict(self):
        return {
            "name": self.name,
            "faculty": self.faculty,
            "need": self.need,
            "give": self.give
        }
