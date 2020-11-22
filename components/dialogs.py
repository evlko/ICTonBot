import telebot
from enum import IntEnum

from components.database.dbworker import DatabaseWorker
from components.core import bot
from data.User import User, UserFactory
from data.subject_list import subject_list
import components.config as config


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
    BACK_FROM_GIVE_SUBJECTS = 10,
    GIVE_SUBJECTS_READY = 11,
    REGISTERED_READY = 12,
    START_SEARCH = 13

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

    print("DEBUG", DatabaseWorker.get_current_state(message.chat.id))
    DatabaseWorker.set_state(message.chat.id, config.UserState.ENTER_NAME)
    print("DEBUG", DatabaseWorker.get_current_state(message.chat.id))


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == config.UserState.ENTER_NAME.value[0])
def read_name(message):
    print("Registered new user with name " + message.text)
    DatabaseWorker.set_name(message.chat.id, message.text)
    DatabaseWorker.set_username(message.chat.id, message.chat.username)

    ask_for_faculty(message)


def ask_for_faculty(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_FACULTY))

    with open("text_messages/ask_for_faculty.txt", "rt", encoding="utf-8") as f:
        message_text = f.read().replace("USERNAME", DatabaseWorker.get_name(message.chat.id))

    bot.send_message(message.chat.id, message_text, reply_markup=markup)

    DatabaseWorker.set_state(message.chat.id, config.UserState.ENTER_FACULTY)


@bot.message_handler(
    func=lambda message: DatabaseWorker.get_current_state(message.chat.id) == config.UserState.ENTER_FACULTY.value[0])
def read_faculty(message):
    DatabaseWorker.set_faculty(message.chat.id, message.text)
    print("Faculty of " + DatabaseWorker.get_name(message.chat.id) + " is " + DatabaseWorker.get_faculty(
        message.chat.id))

    ask_for_needed_subjects(message)


def ask_for_needed_subjects(message):
    subjects = subject_list.keys()

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    selected_subjects = DatabaseWorker.get_needed_subject_list(message.chat.id)

    for subject in subjects:
        if subject in selected_subjects:
            markup.add(telebot.types.InlineKeyboardButton(text=subject + " ✅", callback_data=subject))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subject, callback_data=subject))

    markup.add(telebot.types.InlineKeyboardButton(text="Далее", callback_data=DialogEvent.NEED_SUBJECTS_READY))
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=DialogEvent.BACK_FROM_NEEDED_SUBJECTS))

    with open("text_messages/ask_for_need_subjects.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(chat_id=message.chat.id, text=message_text, reply_markup=markup)
    DatabaseWorker.set_state(message.chat.id, config.UserState.NEEDED_SUBJECT_LIST)


def ask_for_give_subjects(message):
    subjects = subject_list.keys()

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    selected_subjects = DatabaseWorker.get_give_subject_list(message.chat.id)

    for subject in subjects:
        if subject in selected_subjects:
            markup.add(telebot.types.InlineKeyboardButton(text=subject + " ✅", callback_data=subject))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subject, callback_data=subject))

    markup.add(telebot.types.InlineKeyboardButton(text="Далее", callback_data=DialogEvent.GIVE_SUBJECTS_READY))
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=DialogEvent.BACK_FROM_GIVE_SUBJECTS))

    with open("text_messages/ask_for_give_subjects.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
    DatabaseWorker.set_state(message.chat.id, config.UserState.GIVE_SUBJECT_LIST)


def about(message):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ABOUT))

    with open("text_messages/about.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)


def registered(message):
    DatabaseWorker.set_state(message.chat.id, config.UserState.REGISTERED)
    options = ["Начать поиск"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.START_SEARCH))

    with open("text_messages/ready.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)


def search_page(message):
    DatabaseWorker.set_state(message.chat.id, config.UserState.REGISTERED)
    options = ["Повторить поиск"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.START_SEARCH))

    with open("text_messages/search.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    users = DatabaseWorker.best_users_list(message.chat.id)

    if len(users) == 0:
        message_text = "Ой, ни одного пользователя не нашлось"
    else:
        for i, v in enumerate(users):
            message_text += "\n" + str(i + 1) + ". @" + v[1].username

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=message_text,
                          reply_markup=markup)
