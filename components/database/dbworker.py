from vedis import Vedis
import components.config as config


class DatabaseWorker:
    """Singleton class with static methods for database worker."""

    @staticmethod
    def get_current_state(user_id):
        with Vedis(config.db_file) as db:
            try:
                return db[user_id].decode()
            except:
                return config.UserStates.START.value

    @staticmethod
    def set_state(user_id, value) -> bool:
        with Vedis(config.db_file) as db:
            try:
                db[user_id] = value
                return True
            except:
                return False
