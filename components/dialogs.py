from enum import IntEnum

import telebot

import components.config as config
from components.core import bot
from components.database.dbworker import DatabaseWorker
from data.subject_list import subject_list

selected_subjects = []


class DialogEvent(IntEnum):
    START_DIALOG = 1,
    ASK_FOR_NEEDED_SUBJECTS = 2,
    ABOUT = 3,
    BACK_FROM_ASK_NAME = 4,
    ASK_FOR_NAME = 5,
    NEED_SUBJECTS_READY = 6,
    BACK_FROM_NEEDED_SUBJECTS = 7,
    BACK_FROM_ABOUT = 8,
    BACK_FROM_FACULTY = 9,

    # subjects


def welcome_message(message):
    options = ["Начать общение", "О создателях"]
    callbacks = [DialogEvent.ASK_FOR_NAME, DialogEvent.ABOUT]

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option, callback in zip(options, callbacks):
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=callback))

    with open("text_messages/welcome_message.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(message.chat.id, message_text, reply_markup=markup)


def ask_for_name(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(
            telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ASK_NAME))

    with open("text_messages/ask_for_name.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
    DatabaseWorker.set_state(message.chat.id, config.UserState.ENTER_NAME)


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == config.UserState.ENTER_NAME.value[0])
def read_name(message):
    DatabaseWorker.set_username(message.chat.id, message.text)

    ask_for_faculty(message)


def ask_for_faculty(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_FACULTY))

    with open("text_messages/ask_for_faculty.txt", "rt", encoding="utf-8") as f:
        message_text = f.read().replace("USERNAME", DatabaseWorker.get_username(message.chat.id))

    bot.send_message(message.chat.id, message_text, reply_markup=markup)
    DatabaseWorker.set_state(message.chat.id, config.UserState.ENTER_FACULTY)


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == config.UserState.ENTER_FACULTY.value[0])
def read_faculty(message):
    DatabaseWorker.set_faculty(message.chat.id, message.text)

    ask_for_needed_subjects(message)


def ask_for_needed_subjects(message):
    subjects = subject_list.keys()

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for subject in subjects:
        if subject in selected_subjects:
            markup.add(telebot.types.InlineKeyboardButton(text=subject + " ✅", callback_data=subject))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subject, callback_data=subject))

    markup.add(telebot.types.InlineKeyboardButton(text="Готово", callback_data=DialogEvent.NEED_SUBJECTS_READY))
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=DialogEvent.BACK_FROM_NEEDED_SUBJECTS))

    with open("text_messages/ask_for_subjects.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(chat_id=message.chat.id, text=message_text, reply_markup=markup)
    DatabaseWorker.set_state(message.chat.id, config.UserState.NEEDED_SUBJECT_LIST)


def about(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ABOUT))

    with open("text_messages/about.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
