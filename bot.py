#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import Updater, CommandHandler, Job
import logging, yaml, sys, os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filename='bot.log',
    filemode='w',
)

logger = logging.getLogger(__name__)


# Trying to read config
try:
    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile)
except BaseException:
    print "config.yml file is not exists! Please create it first."
    sys.exit()

if config['token'] == '':
    print "Please configure your Telegram bot token"
    sys.exit()

if len(config['files']) == 0:
    print "Please add some files to the config"
    sys.exit()

if config['interval'] == 0 or config['interval'] == '':
    logger.warn('Notify interval is not set. I will send log files every 4 hours')
    config['interval'] = 4*60*60

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update, job_queue):
    if update.message.from_user.username not in config['users']:
        bot.sendMessage(update.message.chat_id,text="Sorry, you are not in the list")
        return

    bot.sendMessage(
        update.message.chat_id,
        parse_mode="Markdown",
        text=(
            "Howdy!\n"
            "Write */cat* to output all configured files,\n"
            "or */cat *_filename_ _filename2_ ' ' to send only _filename_ and _filename2_ (those files must be defined in the config file)"
        )
    )

    start_notifications(bot, job_queue, update.message.chat_id)

def stop(bot, update, job_queue):
    bot.sendMessage(update.message.chat_id, text="Farewell! I'll stop all timers, but you still can use /cat command")
    stop_notifications(bot, job_queue, update.message.chat_id)

def start_notifications(bot, job_queue, chat_id):
    m, s = divmod(config['interval'], 60)
    h, m = divmod(m, 60)
    interval = "%dh:%02dm:%02ds" % (h, m, s)

    bot.sendMessage(
        chat_id,
        parse_mode="Markdown",
        text="Content of those files will be sent every %s: ```\n%s\n```" % (interval, ' '.join(config['files']))
    )

    notification_job = Job(callback_cat, config['interval'], context=chat_id)
    job_queue.put(notification_job, next_t=0.0)

def stop_notifications(bot, job_queue, chat_id):
    for job in job_queue.jobs():
        if job.context == chat_id:
            job.schedule_removal()

def cat_file(bot, chat_id, filename):
    with open(filename, 'rb') as file:
        data = []
        while True:
            data_chunk = file.read(4096)
            if not data_chunk:
                break
            data.append(data_chunk)
    bot.sendMessage(chat_id, parse_mode="Markdown", text="*%s*:" % filename)
    for data_chunk in data:
        bot.sendMessage(chat_id, parse_mode="Markdown", text="```\n%s\n```" % data_chunk)
    bot.sendMessage(chat_id, parse_mode="Markdown", text="*End of file %s*" % filename)

def callback_cat(bot, job):
    for file_name in config['files']:
        cat_file(bot, job.context, file_name)

def cat(bot, update, args=[]):
    for file_name in config['files']:
        if len(args) > 0 and file_name not in args:
            continue
        cat_file(bot, update.message.chat_id, file_name)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(config['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    dp.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("cat", cat, pass_args=True))
    # dp.add_handler(CommandHandler("set", set, pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
