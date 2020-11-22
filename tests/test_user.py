import unittest

from data.User import *


class GenerateUserTestCase(unittest.TestCase):
    """Testing module with unittests for data.User.py"""

    @staticmethod
    def test_new_user():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"], "3")

    @staticmethod
    def test_fake_user():
        user = UserFactory.new_fake_user()

    @staticmethod
    def test_user_to_dict():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"], UserState.START.value[0])
        print(user.to_dict())

    @staticmethod
    def test_user_from_dict():
        data = {"name": "Name", "faculty": "Faculty", "need": ["a", "b"], "give": ["c", "d"], "state": "3"}
        print(UserFactory.from_dict(data))

    @staticmethod
    def test_serialization():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"], UserState.ABOUT.value[0])
        print(serialized(user))

    @staticmethod
    def test_deserialization():
        s = '{"name": "Name", "faculty": "Faculty", "need": ["a", "b"], "give": ["c", "d"], "state": "2"}'
        print(deserialized(s))
