import unittest

from data.User import *


class GenerateUserTestCase(unittest.TestCase):
    """Testing module with unittests for data.User.py"""

    @staticmethod
    def test_new_user():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"])

    @staticmethod
    def test_fake_user():
        user = UserFactory.new_fake_user()

    @staticmethod
    def test_user_to_dict():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"])
        print(user.to_dict())

    @staticmethod
    def test_user_from_dict():
        data = {"name": "Name", "faculty": "Faculty", "need": ["a", "b"], "give": ["c", "d"]}
        print(UserFactory.from_dict(data))

    @staticmethod
    def test_serialization():
        user = UserFactory.new_user("Name", "Faculty", ["a", "b"], ["c", "d"])
        print(serialized(user))

    @staticmethod
    def test_deserialization():
        s = '{"name": "Name", "faculty": "Faculty", "need": ["a", "b"], "give": ["c", "d"]}'
        print(deserialized(s))
