import sys
from pyrogram import idle, Client
from chatbot import app, LOGGER

from chatbot.bot import chat_bot

if len(sys.argv) not in (1, 3, 4):
    quit(1)
else:
    app.start()
    LOGGER.info("Misaki chatbot. Uses Intellivoid's Coffeehouse API.")
    idle()
