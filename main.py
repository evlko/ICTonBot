import telebot

TOKEN = "1245697834:AAERFJK5gT6B_JWpttQYkr7WjYJodcvH5G4"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Приветики")


bot.polling()
