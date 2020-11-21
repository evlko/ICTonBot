import telebot
import time

import components.dialogs as dialogs
from components.core import bot
from components.core import logger
from components.dialogs import DialogEvent


@bot.message_handler(commands=["start", "help"])
def start_messaging(message):
    options = ["Начать общение", "О создателях"]
    callbacks = [DialogEvent.ASK_FOR_NAME, DialogEvent.ABOUT]

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for option, callback in zip(options, callbacks):
        markup.add(telebot.types.InlineKeyboardButton(text=option, callback_data=callback))

    with open("text_messages/welcome_message.txt", "rt", encoding="utf-8") as f:
        message_text = f.read()

    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def on_dialog_event(call):
    dialog_event = DialogEvent(int(call.data))

    if dialog_event == DialogEvent.ASK_FOR_NAME:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        dialogs.ask_for_name(call.message.chat.id)
    elif dialog_event == DialogEvent.ABOUT:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        with open("text_messages/about.txt", "rt", encoding="utf-8") as f:
            text = f.read()
        bot.send_message(call.message.chat.id, text)
    else:
        pass
        # if call.data in dialogs.selected_subjects:
        #     dialogs.selected_subjects.remove(call.data)
        # else:
        #     dialogs.selected_subjects.append(call.data)
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        # dialogs.ask_for_subjects(call.message.chat.id)


if __name__ == "__main__":
    print(DialogEvent.ASK_FOR_NAME, type(DialogEvent.ASK_FOR_NAME))
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as err:
            logger.error(err)
            time.sleep(5)
            print("Internet error!")
