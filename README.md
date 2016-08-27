# Python Telegram Bot Notifier

This is a simple Telegram Bot that will send content of files to your Telegram chat.

## Requirements

- Python 2.7
- python-telegram-bot module

## Installation

```bash
git clone https://github.com/shanginn/py_telegram_notifier && cd py_telegram_notifier
sudo pip install python-telegram-bot --upgrade
```

## Configuration

```bash
mv config.yml.dist config.yml
```

Go to the [@BotFather](https://telegram.me/BotFather) and create a bot.
Put your HTTP API token in config.

Be sure to add your username to the `users` list, otherwise bot will not respond to your actions.

Also you might want to change files list - by default bot will send you content of the `.gitignore` and `config.yml` files.

## Run

```bash
python bot.py
```

To enable notifications every `interval`-seconds write `/start` into your bots chat window.

## Disclaimer

This code was written in 2 hours only as a proof of concept :)
But if you have any questions feel free to contact me.
