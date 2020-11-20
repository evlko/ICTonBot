#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, FACULTY, NEED, GIVE = range(4)


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Добрый день, студент! Этот бот поможет найти тебе товарища, который поможет чего с чем-то по учёбе, '
        'но и ты должен ему помочь взамен! Расскажи мне, как тебя зовут?'
    )

    return NAME


def get_name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("%s зовут %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Отлично! А теперь расскажи мне с какого ты факультета ',
    )

    return FACULTY


def get_faculty(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Дискретка', 'Линал', 'Матан', 'Аналгеом', 'Физика']]
    user = update.message.from_user
    logger.info("%s с факультета %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Отлично, выбери предметы, по которым нужна помощь:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return NEED


def get_need(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Дискретка', 'Линал', 'Матан', 'Аналгеом', 'Физика']]
    user = update.message.from_user
    logger.info("%s хочет получить помощь по %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Как и говорилось в начале, чтобы получить помощь по предмету, ты сам должен что-то предложить. Что это может '
        'быть? ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GIVE


def get_give(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("%s предложит помощь по %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Отлично, твоя анкета готова! Жди ответа!'
    )


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("%s отключился.", user.first_name)
    update.message.reply_text(
        'Если захочешь вернуться - буду ждать :)', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1245697834:AAERFJK5gT6B_JWpttQYkr7WjYJodcvH5G4", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            FACULTY: [MessageHandler(Filters.text & ~Filters.command, get_faculty)],
            NEED: [MessageHandler(Filters.regex('^(Дискретка|Линал|Матан|Аналгеом|Физика)$'), get_need)],
            GIVE: [MessageHandler(Filters.regex('^(Дискретка|Линал|Матан|Аналгеом|Физика)$'), get_give)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
