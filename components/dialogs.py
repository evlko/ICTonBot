import telebot
from enum import IntEnum

from components.core import bot

selected_subjects = []


class DialogEvent(IntEnum):
    START_DIALOG = 1,
    ASK_FOR_NEEDED_SUBJECTS = 2,
    ABOUT = 3,
    BACK_FROM_ASK_NAME = 4,
    ASK_FOR_NAME = 5,
    NEED_SUBJECTS_READY = 6,
    BACK_FROM_NEEDED_SUBJECTS = 7


def ask_for_name(chat_id: int):
    options = ["Назад"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=DialogEvent.BACK_FROM_ASK_NAME))

    with open("text_messages/ask_for_name.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(chat_id, message_text, reply_markup=markup)


def ask_for_subjects(chat_id: int):
    subject_list = ["Дискретка", "Линал", "Матан", "Аналгеом", "Физика"]
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for subject in subject_list:
        if subject in selected_subjects:
            markup.add(telebot.types.InlineKeyboardButton(text=subject + " ✅", callback_data=subject))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subject, callback_data=subject))

    markup.add(telebot.types.InlineKeyboardButton(text="Готово", callback_data=DialogEvent.NEED_SUBJECTS_READY))
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=DialogEvent.BACK_FROM_NEEDED_SUBJECTS))

    with open("text_messages/ask_for_subjects.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(chat_id, message_text, reply_markup=markup)
