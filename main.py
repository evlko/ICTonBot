import telebot

TOKEN = "1245697834:AAERFJK5gT6B_JWpttQYkr7WjYJodcvH5G4"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_messaging(message):
    subjects = ['Дискретка', 'Линал', 'Матан', 'Аналгеом', 'Физика', 'Готово']
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for each in subjects:
        markup.add(telebot.types.InlineKeyboardButton(text=each, callback_data=each))

    bot.reply_to(message, "Привет, выбери предметы, по которым тебе нужна помощь:", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
