# Python Telegram Bot Notifier

This is a simple Telegram Bot that will send content of files to your Telegram chat.

Article in russian about this bot: http://shanginn.ru/telegram-bot-notifier/

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

Also you might want to change `files` list - by default bot will send you content of the `.gitignore` and `config.yml` files.

## Run

```bash
python bot.py
```

To enable notifications every `interval`-seconds write `/start` into your bots chat window.

## TODO

I have ideas about some neat features, that could be implementet, but I don't have time for this, so feel free to do pull requests :)
Really powerful thing would be ability to edit config file from chat, but you need to do password protection first, because such access is very unsecure.

* `/unlock_config <password>` - enable ability to edit config from chat. After sending this command you must delete message with password
* `/set_interval <interval>` - change interval of the messages
* `/add_file <path>` and `/remove_file <path>` - add\\remove files from allowed files list
* `/watch <path>` - watch the file and send changes in realtime. Ofc you need `/unwatch <path>`
* `/lock_config` - after all this you need to lock config file again(and after some time, for example, 5 minutes you must lock it automatically)
* `/head` and `/tail` - \*nix-like `head` and `tail` commands.

## Disclaimer

This code was written in several hours only as proof of concept :)

But if you have any questions feel free to contact me.

Enjoy! :)
