import telebot
import time
import json

import components.dialogs as dialogs
from components.core import bot
from components.core import logger
from components.dialogs import DialogEvent


@bot.message_handler(commands=["start", "help"])
def start_messaging(message):
    dialogs.welcome_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: str.isnumeric(call.data))
def on_dialog_event(call):
    """A function that catches dialog event callbacks."""
    print(call.data)
    dialog_event = DialogEvent(int(call.data))
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if dialog_event == DialogEvent.ASK_FOR_NAME:
        dialogs.ask_for_name(call.message.chat.id)
    elif dialog_event == DialogEvent.ABOUT:
        dialogs.about(call.message.chat.id)
    elif dialog_event in [DialogEvent.BACK_FROM_ASK_NAME, DialogEvent.BACK_FROM_ABOUT]:
        dialogs.welcome_message(call.message.chat.id)
    elif dialog_event == DialogEvent.NEED_SUBJECTS_READY:
        bot.send_message(call.message.chat.id, "Окей")
    elif dialog_event == DialogEvent.BACK_FROM_NEEDED_SUBJECTS:
        dialogs.ask_for_faculty(call.message.chat.id)
    elif dialog_event == DialogEvent.BACK_FROM_FACULTY:
        dialogs.ask_for_name(call.message.chat.id)
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


if __name__ == "__main__":
    print(DialogEvent.ASK_FOR_NAME, type(DialogEvent.ASK_FOR_NAME))
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            logger.error(err)
            time.sleep(5)
            print("Internet error!")
