import random


def generate_hash() -> int:
    return random.getrandbits(128)
