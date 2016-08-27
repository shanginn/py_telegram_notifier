#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import logging, random, json

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

wait_list = []
chat_list = {}
stats = {}

def start(bot, update):
    if update.message.chat_id in wait_list:
        bot.sendMessage(update.message.chat_id, text='Я скоро найду вам кого-нибудь, не переживайте :)')
    else:
        bot.sendMessage(update.message.chat_id, text='Ищу нужного вам человека...')
        if len(wait_list) > 0:
            random.shuffle(wait_list)
            chat_to_id = wait_list.pop()

            chat_list[chat_to_id] = update.message.chat_id
            chat_list[update.message.chat_id] = chat_to_id

            if update.message.chat_id in wait_list:
                del wait_list[update.message.chat_id]

            bot.sendMessage(update.message.chat_id, text='Вы соединены, скажите "Привет"!')
        else:
            bot.sendMessage(update.message.chat_id, text='Пока никого нет, подождите пожалуйста')
            wait_list.append(update.message.chat_id)

def end(bot, update):
    if update.message.chat_id in chat_list:
        if chat_list[update.message.chat_id] in chat_list:
            del chat_list[chat_list[update.message.chat_id]]
        bot.sendMessage(update.message.chat_id, text='Завершаю разговор, надеюсь, вам понравилось. :)')
        del chat_list[update.message.chat_id]
    elif update.message.chat_id in wait_list:
        bot.sendMessage(update.message.chat_id, text='Скоро бы обязательно кто-то нашелся!')
        wait_list.remove(update.message.chat_id)

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    if update.message.chat_id in chat_list:
        msg = update.message.text
        statictic(msg)
        bot.sendMessage(chat_list[update.message.chat_id], text=msg)

def statictic(msg):
    for word in msg.split(' '):
        if word in stats:
            stats[word] += 1
        else:
            stats[word] = 1

def get_stats(bot, update):
    bot.sendMessage(chat_list[update.message.chat_id], text=json.dumps(stats))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("200483686:AAFUKhTwBiiN0cXWYV3Zu03Cpd9bqAPLrbs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("stats", get_stats)
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("end", end)
    dp.addTelegramCommandHandler("help", help)

    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()