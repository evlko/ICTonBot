from enum import Enum

TOKEN = "1245697834:AAERFJK5gT6B_JWpttQYkr7WjYJodcvH5G4"
db_file = "database.vdb"


class UserStates(Enum):
    START = "0",
    ENTER_NAME = "1",
    ENTER_FACULTY = "2",
    NEEDED_SUBJECT_LIST = "3",
    ABOUT = "4",
    GIVE_SUBJECT_LIST = "5",
