import telebot
import config
import typing

bot = telebot.TeleBot(config.TOKEN)

selected_subjects = []


@bot.message_handler(commands=['start', 'help'])
def start_messaging(message):
    subjects = ['Начать общение', 'О создателях']

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for each in subjects:
        markup.add(telebot.types.InlineKeyboardButton(text=each, callback_data=each))

    with open('text_messages/welcome_message.txt', 'rt', encoding='utf-8') as f:
        text = f.read()

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'Готово':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Ну и хорошо')
    elif call.data == 'Начать общение':
        ask_for_subjects(call.message.chat.id)
    elif call.data == 'О создателях':
        with open('text_messages/about.txt', 'rt', encoding='utf-8') as f:
            text = f.read()
        bot.send_message(call.message.chat.id, text)
    else:
        if call.data in selected_subjects:
            selected_subjects.remove(call.data)
        else:
            selected_subjects.append(call.data)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        ask_for_subjects(call.message.chat.id)


def ask_for_subjects(chat_id: int):
    subjects = ['Дискретка', 'Линал', 'Матан', 'Аналгеом', 'Физика', 'Готово']
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for each in subjects:
        if each in selected_subjects:
            markup.add(telebot.types.InlineKeyboardButton(text=each + " ✅", callback_data=each))
        else:
            markup.add(telebot.types.InlineKeyboardButton(text=each, callback_data=each))
    bot.send_message(chat_id, "Пожалуйста, выбери предметы, по которым тебе нужна помощь:", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
