import random
import telebot

import components.config

bot = telebot.TeleBot(components.config.TOKEN)
logger = telebot.logger


def generate_hash() -> int:
    return random.getrandbits(128)
