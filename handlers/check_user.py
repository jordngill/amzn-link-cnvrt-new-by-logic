# (c) @AmznUsers | Jordan Gill

import datetime

import config
import logging

from handlers.database import Database

DB_URL = config.DB_URL
DB_NAME = config.DB_NAME
LOG_CHANNEL = config.LOG_CHANNEL

db = Database(DB_URL, DB_NAME)

async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)
        if LOG_CHANNEL:
            await bot.send_message(
                LOG_CHANNEL,
                f"#𝐍𝐞𝐰𝐔𝐬𝐞𝐫\n\n᚛› 𝐈𝐃 - `{cmd.from_user.id}`\n᚛› 𝐍𝐚𝐦𝐞 - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})",
            )
        else:
            logging.info(f"#NewUser :- Name : {cmd.from_user.first_name} ID : {cmd.from_user.id}")

    ban_status = db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
            datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned to Use This Bot ", quote=True)
            return
    await cmd.continue_propagation()
