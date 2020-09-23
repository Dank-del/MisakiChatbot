import sys
from pyrogram import idle, Client
from chatbot import app, LOGGER

from chatbot.bot import chat_bot

if len(sys.argv) not in (1, 3, 4):
    quit(1)
else:
    app.start()
    LOGGER.info("Misaki chatbot.\n " \
    "Uses Intellivoid's Coffeehouse API.\n" \
    "Originally Written by @TheRealPhoenix on Telegram.\n Reworked by t.me/dank_as_fuck owo")
    LOGGER.info("Your bot is now online. Check .help for help!")
    idle()
