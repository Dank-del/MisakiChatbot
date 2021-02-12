from time import time
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from coffeehouse.lydia import LydiaAI
from coffeehouse.api import API
from coffeehouse.exception import CoffeeHouseError as CFError

from chatbot import app, LOGGER, CF_API_KEY, NAME
import chatbot.bot.database.chatbot_db as db


CoffeeHouseAPI = API(CF_API_KEY)
api_client = LydiaAI(CoffeeHouseAPI)


prvt_message = '''
Misaki - v0.1\n Using Coffeehouse AI from @Intellivoid\n Click /help to know more :D
'''

grp_message = '''
Hi, I'm Misaki
'''

@app.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start(client, message):
    self = await app.get_me()
    busername = self.username
    if message.chat.type != "private":
        await message.reply_text(grp_message)
        return
    else:
        buttons = [[InlineKeyboardButton("Managed by", url="https://t.me/dank_as_fuck"),
                    ]]
        await message.reply_text(prvt_message, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = """
    **Misaki is a chatbot which uses @Intellivoid's Coffeehouse AI.**\n\n
Coffeehouse Lydia AI can actively chat and learn from you, it gets better everytime.
"""
    self = await app.get_me()
    busername = self.username

    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Click here",
                url=f"t.me/{busername}?start=help")]])
        await message.reply("Contact me in PM",
                            reply_markup=buttons)
    else:
        buttons = [[InlineKeyboardButton("Learn more", url="https://coffeehouse.intellivoid.net"),
                    InlineKeyboardButton('Docs', url=f"https://docs.intellivoid.net")]]
        await message.reply_text(help_text, reply_markup=InlineKeyboardMarkup(buttons))

def check_message(client, msg):
    reply_msg = msg.reply_to_message
    if NAME.lower() in msg.text.lower():
        return True
    if reply_msg and reply_msg.from_user is not None:
        if reply_msg.from_user.is_self:
            return True
    return False


@app.on_message(filters.text & filters.group)
def chatbot_grp(client, message):
    msg = message
    if not check_message(client, msg):
        return
    user_id = msg.from_user.id

    if not user_id in db.USERS:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)

    sesh: str
    sesh, exp = db.get_ses(user_id)
    query = msg.text
    if int(exp) < time():
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        sesh, exp = ses_id, expires
        
    try:
        app.send_chat_action(msg.chat.id, "typing")
        response = api_client.think_thought(sesh, query)
        msg.reply_text(response)
    except CFError as e:
        app.send_message(chat_id=msg.chat.id, text=f"An error occurred:\n`{e}`", parse_mode="md")


@app.on_message(filters.text & filters.private)
def chatbot_pvt(client, message):
    msg = message
    user_id = msg.from_user.id

    if not user_id in db.USERS:
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)

    sesh: str
    sesh, exp = db.get_ses(user_id)
    query = msg.text
    if int(exp) < time():
        ses = api_client.create_session()
        ses_id = str(ses.id)
        expires = str(ses.expires)
        db.set_ses(user_id, ses_id, expires)
        sesh, exp = ses_id, expires

    try:
        app.send_chat_action(msg.chat.id, "typing")
        response = api_client.think_thought(sesh, query)
        msg.reply_text(response)
    except CFError as e:
        app.send_message(chat_id=msg.chat.id, text=f"An error occurred:\n`{e}`", parse_mode="md")
