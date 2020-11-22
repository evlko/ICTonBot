from vedis import Vedis

import components.config as config
from data.User import *


class DatabaseWorker:
    """Singleton class with static methods for database worker."""

    @staticmethod
    def get_username(user_id) -> str:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.name

    @staticmethod
    def set_username(user_id, name: str):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.name = name
            print(serialized(user))

            db[user_id] = serialized(user)

    @staticmethod
    def get_faculty(user_id) -> str:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.faculty

    @staticmethod
    def set_faculty(user_id, faculty: str):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.faculty = faculty
            print(serialized(user))

            db[user_id] = serialized(user)

    @staticmethod
    def get_current_state(user_id) -> str:
        with Vedis(config.db_file) as db:
            try:
                return deserialized(db[user_id].decode()).state
            except:
                return config.UserState.START.value[0]

    @staticmethod
    def set_state(user_id, state: UserState):
        with Vedis(config.db_file) as db:
            try:
                user = deserialized(db[user_id].decode())
                user.state = state.value[0]
                print(serialized(user))

                db[user_id] = serialized(user)
            except KeyError:
                user = UserFactory.new_fake_user()
                user.state = state.value[0]
                db.update({user_id: serialized(user)})

                print(serialized(user))
