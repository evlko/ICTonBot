import unittest

from components.core import generate_hash


class GenerateHashTestCase(unittest.TestCase):
    def debug(self) -> None:
        """Showcase of 128-bit hash generation."""
        print(generate_hash())
