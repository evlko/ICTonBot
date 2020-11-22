import time
import telebot

import components.config as config
import components.dialogs as dialogs
from components.config import UserState
from components.core import bot, logger
from components.database.dbworker import DatabaseWorker
from components.dialogs import DialogEvent
from data.subject_list import subject_list


@bot.message_handler(commands=["start", "help"])
def start_messaging(message):
    dialogs.welcome_message(message)


@bot.callback_query_handler(func=lambda call: str.isnumeric(call.data))
def on_dialog_event(call):
    """A function that catches dialog event callbacks."""
    print(call.data)
    dialog_event = DialogEvent(int(call.data))
    # bot.delete_message(call.message.chat.id, call.message.message_id)

    if dialog_event == DialogEvent.ASK_FOR_NAME:
        dialogs.ask_for_name(call.message)
    elif dialog_event == DialogEvent.ABOUT:
        DatabaseWorker.set_state(call.message.chat.id, config.UserState.ABOUT)
        dialogs.about(call.message)
    elif dialog_event in [DialogEvent.BACK_FROM_ASK_NAME, DialogEvent.BACK_FROM_ABOUT]:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        DatabaseWorker.set_state(call.message.chat.id, config.UserState.START)
        dialogs.welcome_message(call.message)
    elif dialog_event == DialogEvent.NEED_SUBJECTS_READY:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Окей")
    elif dialog_event == DialogEvent.BACK_FROM_NEEDED_SUBJECTS:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        dialogs.ask_for_faculty(call.message)
    elif dialog_event == DialogEvent.BACK_FROM_FACULTY:
        dialogs.ask_for_name(call.message)
    elif call.data:
        pass
        # if call.data in dialogs.selected_subjects:
        #     dialogs.selected_subjects.remove(call.data)
        # else:
        #     dialogs.selected_subjects.append(call.data)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # dialogs.ask_for_subjects(call.message.chat.id)


@bot.callback_query_handler(func=lambda call: not str.isnumeric(call.data))
def on_string_callback(call):
    """A callback function that is used to catch string callbacks (for example for subjects)"""
    print("String callback was passed: " + call.data)
    clicked = str(call.data)

    subjects = subject_list.keys()

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for subject in subjects:
        if subject == clicked:
            markup.add(telebot.types.InlineKeyboardButton(text=subject + " ✅", callback_data=subject))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=subject, callback_data=subject))

    markup.add(telebot.types.InlineKeyboardButton(text="Готово", callback_data=DialogEvent.NEED_SUBJECTS_READY))
    markup.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=DialogEvent.BACK_FROM_NEEDED_SUBJECTS))

    with open("text_messages/ask_for_subjects.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message_text,
                          reply_markup=markup)


if __name__ == "__main__":
    print(DialogEvent.ASK_FOR_NAME, type(DialogEvent.ASK_FOR_NAME))
    DatabaseWorker.set_state("192767028", UserState.START)
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            logger.error(err)
            time.sleep(5)
            print("Internet error!")
