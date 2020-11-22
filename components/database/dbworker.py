from vedis import Vedis

import components.config as config
from data.User import *


class DatabaseWorker:
    """Singleton class with static methods for database worker."""

    @staticmethod
    def best_users_list(user_id):
        with Vedis(config.db_file) as db:
            this_user = deserialized(db[user_id].decode())
            ret = []
            with open("components/database/userlist.txt", "rt") as f:
                keys = f.read(user_id).split("\n")

            for k in keys:
                print(k, user_id)
                if k == user_id or len(k) == 0:
                    continue
                try:
                    user = deserialized(db[k].decode())
                    ret.append(
                        [len(set(user.give_subjects) & set(this_user.need_subjects)) + len(set(user.need_subjects) & set(
                            this_user.give_subjects)), user])
                except KeyError:
                    continue

            ret = sorted(ret)[::-1]
            if len(ret) <= 10:
                return ret
            return ret[:10]

    @staticmethod
    def contain_user(user_id) -> bool:
        with Vedis(config.db_file) as db:
            return user_id in db

    @staticmethod
    def get_name(user_id) -> str:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.name

    @staticmethod
    def set_name(user_id, name: str):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.name = name
            print(serialized(user))

            db[user_id] = serialized(user)

    @staticmethod
    def get_username(user_id) -> str:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.username

    @staticmethod
    def set_username(user_id, username: str):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.username = username
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
    def get_needed_subject_list(user_id) -> typing.List[str]:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.need_subjects

    @staticmethod
    def set_needed_subject_list(user_id, subject_list: typing.List[str]):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.need_subjects = subject_list
            print(serialized(user))

            db[user_id] = serialized(user)

    @staticmethod
    def get_give_subject_list(user_id) -> typing.List[str]:
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            return user.give_subjects

    @staticmethod
    def set_give_subject_list(user_id, subject_list: typing.List[str]):
        with Vedis(config.db_file) as db:
            user = deserialized(db[user_id].decode())
            user.give_subjects = subject_list
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
                with open("components/database/userlist.txt", "at") as f:
                    f.write(str(user_id) + "\n")

                user = UserFactory.new_fake_user()
                user.state = state.value[0]
                db.update({user_id: serialized(user)})

                print(serialized(user))
