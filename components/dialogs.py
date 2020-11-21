import telebot
from enum import IntEnum

from components.database.dbworker import DatabaseWorker
from components.core import bot
from data.User import User, UserFactory
from data.subject_list import subject_list
import components.config as config

selected_subjects = []
new_user = UserFactory.new_fake_user()


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
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ASK_NAME))

    with open("text_messages/ask_for_name.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
    # bot.send_message(message.chat.id, message_text, reply_markup=markup)
    # bot.register_next_step_handler(message, read_name)
    print(DatabaseWorker.get_current_state(message.chat.id))
    DatabaseWorker.set_state(message.chat.id, config.UserStates.ENTER_NAME.value)


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == str(config.UserStates.ENTER_NAME.value))
def read_name(message):
    print("Registered new user with name " + message.text)
    new_user.name = message.text

    ask_for_faculty(message)


def ask_for_faculty(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_FACULTY))

    with open("text_messages/ask_for_faculty.txt", "rt", encoding="utf-8") as f:
        message_text = f.read().replace("USERNAME", new_user.name)

    bot.send_message(message.chat.id, message_text, reply_markup=markup)
    # bot.register_next_step_handler(message, read_faculty)
    DatabaseWorker.set_state(message.chat.id, config.UserStates.ENTER_FACULTY.value)


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == str(
        config.UserStates.ENTER_FACULTY.value))
def read_faculty(message):
    print("Faculty of " + new_user.name + " is " + message.text)
    new_user.faculty = message.text

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
    DatabaseWorker.set_state(message.chat.id, config.UserStates.NEEDED_SUBJECT_LIST)


def about(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ABOUT))

    with open("text_messages/about.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
