# (c) @AmznUsers | Jordan Gill

import asyncio
import os ,sys
import json
import traceback
import logging
import config
import time

import pyromod
from asyncio.exceptions import TimeoutError

from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyromod.listen.listen import ListenerTypes
from pyrogram import Client, idle
from pyrogram import enums, filters, StopPropagation
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageNotModified

from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired,
    UserAlreadyParticipant
)

from handlers.check_user import handle_user_status
from handlers.database import Database
from handlers.amazon import Amazon
from utils.extractors import extract_links
from aiohttp import web
from route import web_server

LOG_CHANNEL = config.LOG_CHANNEL
AUTH_USERS = config.AUTH_USERS
DB_URL = config.DB_URL
DB_NAME = config.DB_NAME
BOT_TYPE_PUBLIC = config.BOT_TYPE_PUBLIC
FORWARD_CHANNEL_NUMBER = config.FORWARD_CHANNEL_NUMBER

db = Database(DB_URL, DB_NAME)

Bot = Client(
    "Amazon-bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)

async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("⛔ Process Cancelled.")
        return True
    return False

@Bot.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Bot.on_message(filters.command("start") & filters.private)
async def startprivate(client: Client, message: Message):
    chat_id = message.from_user.id
    if not db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#𝐍𝐞𝐰𝐔𝐬𝐞𝐫\n\n᚛› 𝐈𝐃 - `{message.from_user.id}`\n᚛› 𝐍𝐚𝐦𝐞 - [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
            )
        else:
            logging.info(
                f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}")
    joinButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AmznUsers"),
                InlineKeyboardButton(
                    "SUPPORT GROUP", url="https://t.me/AmznUsers"
                ),
            ]
        ]
    )
    welcomed = f"""**Hello {message.from_user.mention}, I am AMAZON Affiliate Bulk Link Convertor**, 

• **I am AMAZON Affiliate Bulk Link Convertor.**
• __If send me a post which has urls, texts & images... Than i wiil replace all urls with AMAZON Affiliate URL automatic.__
• __I can convert a list of amazon urls.__
• **I Can Autopost To your channels (you can add multiple channels at once.)** Hit /autopost to know How...
• **I can automatic add your channel link in footer(down side) of your post. but first add your channel link.** hit /help to know how? 
• **I can instantly forward (or copy) messages from various Telegram chats (private/public channels, private/public groups, direct chats, and bots) to one or multiple chats upon their receipt.**

💁‍♀️ Hit 👉 /help To Get Help.
💻 Hit 👉 /cmd to know about all commands."""

    await message.reply_text(welcomed, reply_markup=joinButton, quote=True)
    raise StopPropagation

@Bot.on_message(filters.command("features") & filters.private)
async def features(client: Client, message: Message):
    chat_id = message.from_user.id
    if not db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#𝐍𝐞𝐰𝐔𝐬𝐞𝐫\n\n᚛› 𝐈𝐃 - `{message.from_user.id}`\n᚛› 𝐍𝐚𝐦𝐞 - [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
            )
        else:
            logging.info(
                f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}")

    welcomed = f"""**Hello {message.from_user.mention}, I am AMAZON Affiliate Bulk Link Convertor**, 

• **I am AMAZON Affiliate Bulk Link Convertor.**
• __If send me a post which has urls, texts & images... Than i wiil replace all urls with AMAZON Affiliate URL automatic.__
• __I can convert a list of amazon urls.__
• **I Can Autopost To your channels (you can add multiple channels at once.)** Hit /autopost to know How...
• **I can automatic add your channel link in footer(down side) of your post. but first add your channel link.** hit /help to know how? 
• **I can instantly forward (or copy) messages from various Telegram chats (private/public channels, private/public groups, direct chats, and bots) to one or multiple chats upon their receipt.**

💁‍♀️ Hit 👉 /help To Get Help.
💻 Hit 👉 /cmd to know about all commands.

**Made with 💖 by @AmznUsers**"""

    return await message.reply_text(welcomed, quote=True)
 
@Bot.on_message(filters.command("help") & filters.private)
async def help(client: Client, message: Message):
    chat_id = message.from_user.id
    if not db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)
    help = f"""Hello {message.from_user.mention}, I am AMAZON Affiliate Bulk Link Convertor,

- **To Link AMAZON TAG: Type** `/set_tag` than a single space than paste your AMAZON TAG **(see example to understand more...)**

To Link Now: Just Type 👇 
 `/set_tag<space>your-amazon-tag` 
(See Example.👇)

Example:
`/set_tag AmznUsers-21`

- To Add Channel: Just Type 👇 
 `/add_footer_channel<space>your-channel-link` 
(See Example.👇)

Example:
`/add_footer_channel @AmznUsers`

🤘 **Hit** 👉 /features __To Know More Features Of This Bot.__
🔗 **Hit** 👉 /set_tag __To Know More About How To Link AMAZON affiliate tag To This Bot.__
💁‍♀️ **Hit** 👉 /help __To Get Help.__
💻 **Hit** 👉 /cmd __To know about all commands.__

- **Message @AmznUsers For More Help -**"""

    await message.reply_text(help, quote=True)

@Bot.on_message(filters.command("cmd") & filters.private)
async def cmd(client: Client, message: Message):
    data = await client.get_me()
    chat_id = message.from_user.id
    if not db.is_user_exist(chat_id):
        db.add_user(chat_id)
    cmd = f"""**Hello {message.from_user.mention}, I am {data.mention}**,

- /start -To start the bot.

- /help - To get help.

- /settings - To setup your account Settings

- /id - To get the current Chat ID

- /autopost - To add auto forward channel to the bot. (*You can add multiple channels... Channel IDs separated by the space)
Example: /autopost -100987654322 -100123456780

- /remove_autopost - To remove auto forward channel from the bot. (*You can remove multiple channels... Channel IDs separated by the space)
Example: /remove_autopost -100987654322 -100123456780

- /add_forward_channel - To add auto copy channel to the bot.
Example: /add_forward_channel -100987654322

- /remove_forward_channel - To remove auto copy channel from the bot.
Example: /remove_forward_channel -100987654322

- /add_footer_channel - To add custom Footer Channel Username
Example: /add_footer_channel @AmznUsers

- /remove_footer_channel - To remove custom Footer Channel Username

- /connect - To connect your Telegram Account to bot (*Required for Auto Messages Copy)

- /set_tag (space) Affiliate-tag - To add Amazon Affiliate Tag to bot.

- /unset_tag - To remove Amazon Affiliate Tag from bot.

- /report - To report any Issues or bugs to Admins

- Message @AmznUsers For More Help -"""

    await message.reply_text(cmd, quote=True)

@Bot.on_message(filters.command("settings") & filters.private)
async def opensettings(bot, cmd):
    user_id = cmd.from_user.id
    await cmd.reply_text(
        f"`Here You Can Set Your Settings:`\n\nSuccessfully setted notifications to **{db.get_notif(user_id)}**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"NOTIFICATION  {'🔔' if ((db.get_notif(user_id)) is True) else '🔕'}",
                        callback_data="notifon",
                    )
                ],
                [InlineKeyboardButton("❎", callback_data="closeMeh")],
            ]
        ),
    )

@Bot.on_message(filters.command('restart') & filters.private)
async def restart_bot(bot: Client, message: Message):  
    if message.from_user.id not in AUTH_USERS:
        return
    msg = await message.reply("Restarting")
    os.execl(sys.executable, sys.executable, "main.py")
    
    
@Bot.on_message(filters.command("stats") & filters.private)
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    await m.reply_text(
        text=f"**Total Users in Database 📂:** `{db.total_users_count()}`\n\n**Total Users with Notification Enabled 🔔 :** `{db.total_notif_users_count()}`",
        quote=True
    )

@Bot.on_message(filters.command("id"))
async def id(bot: Client, message: Message):
    msg = ""
    if message.chat.type == enums.ChatType.PRIVATE:
        msg += f"**User ID:** `{message.from_user.id}`"
    elif message.chat.type == enums.ChatType.CHANNEL:
        msg += (
            f"**{str(message.chat.type.value).capitalize()} Name:** `{message.chat.title}`\n"
            f"**{str(message.chat.type.value).capitalize()} ID:** `{message.chat.id}`\n\n"
        )
    else:
        msg += (
            f"**{str(message.chat.type.value).capitalize()} Name:** `{message.chat.title}`\n"
            f"**{str(message.chat.type.value).capitalize()} ID:** `{message.chat.id}`\n\n"
            f"**{message.from_user.first_name} {message.from_user.last_name}'s ID:** `{message.from_user.id}`"
        )

    if message.chat.type == enums.ChatType.CHANNEL:
        return await message.edit(msg)

    await message.reply(msg, quote=True)

@Bot.on_message(filters.command("tagAuthUser") & filters.private)
async def tagauthuser(bot: Client, message: Message):
    if message.from_user.id not in config.AUTH_USERS:
        return

    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the User ID of the user along with the command to whom you wan't to Authorize for using tags.\n\n"
            "\n**Eg:** `/tagauthuser 1166666205`\n\n",
            quote=True
        )
    else:
        for userID in message.command[1:]:
            if user := db.get_user(userID):
                if user.get("tagauth", "") == "authorised":
                    await message.reply(f"`{userID}` is already Authorized for using tags.", quote=True)
                else:
                    db.set_tagauthuser(userID)
                    await message.reply(f"Successfully Authorized `{userID}` for using tags.", quote=True)
            else:
                return await message.reply(f"`{userID}` haven't started the bot before.\n\n**Ask him to start it once before.**", quote=True)

@Bot.on_message(filters.command("tagUnAuthUser") & filters.private)
async def tagUnAuthUser(bot: Client, message: Message):
    if message.from_user.id not in config.AUTH_USERS:
        return

    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the User ID of the user along with the command to whom you wan't to Unauthorize for using tags.\n\n"
            "\n**Eg:** `/tagUnAuthUser 1166666205`\n\n",
            quote=True
        )
    else:
        for userID in message.command[1:]:
            if user := db.get_user(userID):
                if user.get("tagauth", "") == "authorised":
                    db.remove_tagauthuser(userID)
                    await message.reply(f"Successfully Unauthorized `{userID}` for using tags.", quote=True)
                else:
                    await message.reply(f"`{userID}` is not Authorized for using tags.", quote=True)
            else:
                return await message.reply(f"`{userID}` haven't started the bot before.\n\n**Ask him to start it once before.**", quote=True)

@Bot.on_message(filters.command("forwardAuthUser") & filters.private)
async def forwardauthuser(bot: Client, message: Message):
    if message.from_user.id not in config.AUTH_USERS:
        return

    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the User ID of the user along with the command to whom you wan't to Authorize for forwarding.\n\n"
            "\n**Eg:** `/forwardauthuser 1166666205`\n\n",
            quote=True
        )
    else:
        for userID in message.command[1:]:
            if user := db.get_user(userID):
                if user.get("forwardauth", "") == "authorised":
                    await message.reply(f"`{userID}` is already Authorized for forwarding.", quote=True)
                else:
                    db.set_forwardauthuser(userID)
                    await message.reply(f"Successfully Authorized `{userID}` for forwarding.", quote=True)
            else:
                return await message.reply(f"`{userID}` haven't started the bot before.\n\n**Ask him to start it once before.**", quote=True)

@Bot.on_message(filters.command("forwardUnAuthUser") & filters.private)
async def forwardUnAuthuser(bot: Client, message: Message):
    if message.from_user.id not in config.AUTH_USERS:
        return

    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the User ID of the user along with the command to whom you wan't to Unauthorize from forwarding.\n\n"
            "\n**Eg:** `/forwardUnAuthuser 1166666205`\n\n",
            quote=True
        )
    else:
        for userID in message.command[1:]:
            if user := db.get_user(userID):
                if user.get("usertype", "") == "authorised":
                    db.remove_forwardauthuser(userID)
                    await message.reply(f"Successfully Unauthorized `{userID}` for forwarding.", quote=True)
                else:
                    await message.reply(f"`{userID}` is not Authorized for forwarding.", quote=True)
            else:
                return await message.reply(f"`{userID}` haven't started the bot before.\n\n**Ask him to start it once before.**", quote=True)

@Bot.on_message(filters.command("list_autopost_channel") & filters.private)
async def addChannelToDB(bot: Client, message: Message):
    channellist = db.get_all_forward_channel(message.from_user.id)
    if len(channellist) == 0:
        await message.reply(
            "**You have not added any Forward Channel.**\n\n"
            "To Add the bot to the channel and send /id to get the channel ID.\n"
            "**Eg:** `/autopost -10012345678`\n\n",
            quote=True
        )
    else:
        msg ="**List of Forward Channels:**\n\n"
        for i, channel in enumerate(channellist):
            msg += f"{i+1}) `{channel['title']}({channel['id']})`\n"

        await message.reply(msg, quote=True)


@Bot.on_message(filters.command("autopost") & filters.private)
async def addChannelToDB(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the Channel ID along with the command\n\n"
            "Add the bot to the channel and send /id to get the channel ID.\n"
            "\n**Eg:** `/autopost -10012345678`\n\n\n\nNote: This Commad Sends The Post To Added \nAutopost Channel Ids Whenever Something Is Forwarded In Bot\nImportant : Bot Should Be Admin In Channel And Group Of The Given Ids",
            quote=True
        )
    else:
        print(message.command[1])
        try:
            z = await bot.resolve_peer(peer_id= int(message.command[1]))
        except Exception as e:
            print("Resolve ___________>",e)
        try:
            channel = await bot.get_chat(int(message.command[1]))
        except:
            return await message.reply("Kindly add the bot to the channel with Admin Rights, before sending it to me.", quote=True)

        # if channel.type != enums.ChatType.CHANNEL:
        #     return await message.reply("The Chat ID should of a channel only.\n\nAdd the bot to the channel and send /id to get the channel ID.", quote=True)

        if len(db.get_all_forward_channel(message.from_user.id)) == int(FORWARD_CHANNEL_NUMBER):
            return await message.reply(f"**Oops Max limit of adding forward channel is get exceeded.**\nSo first remove already added forward channel using /remove_autopost. \n\n Contact 👉 @AvishkarBots if you feels it bug.", quote=True)

        db.add_forward_channel(message.from_user.id, {"id": channel.id, "title": channel.title})
        await message.reply(f"Successfully added `{channel.title} ({channel.id})` to the Database for Amazon Links Forwarding.", quote=True)

@Bot.on_message(filters.command("remove_autopost") & filters.private)
async def removeChannelToDB(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the Channel ID along with the command\n\n"
            "\n**Eg:** `/remove_autopost -10012345678`\n\n"
            "For get id send /id to get the channel ID in channel which you want to remove.\n\nSend The Id Of Channel From Which You Want To Remove Forwarding",
            quote=True
        )
    else:
        channelIds = message.command[1:]
        for channel in channelIds:
            savedchannel = db.get_all_forward_channel(message.from_user.id)
            for i in savedchannel :
                if str(i["id"]) == channel :
                    db.remove_forward_channel(message.from_user.id, {"id": i["id"], "title": i["title"]})
                    return await message.reply(f"Successfully Removed `{i['title']} ({channel})` from the Database for Amazon Links Forwarding.", quote=True)
            
            return await message.reply(f"No such channel id `({channel})` in the Database for Amazon Links Forwarding.", quote=True)

@Bot.on_message(filters.command("list_forward_channel") & filters.private)
async def addChannelToDB(bot: Client, message: Message):
    channellist = db.get_all_copy_channel(message.from_user.id)
    msg ="**List of Forward Channels:**\n\n"
    for c in channellist:
        msg += f"**Label:** `{c['label']}`\n\n**Sources:**\n"
        for i, channel in enumerate(c['source']):
            msg += f"{i+1}) `{channel['title']}({channel['id']})`\n"
        msg += "\n**Destination:**\n"
        for i, channel in enumerate(c['destination']):
            msg += f"{i+1}) `{channel['title']}({channel['id']})`\n"
        msg += f"\n{'='*25}"

    await message.reply(msg, quote=True)

@Bot.on_message(filters.command("add_forward_channel") & filters.private)
async def addCopyChannelToDB(bot: Client, message: Message):
    if db.get_forwardauthuser(message.from_user.id) != "authorised":
        print(db.get_forwardauthuser(message.from_user.id))
        return await message.reply("You aren't authorized to use Auto Forward feature.", quote=True)

    if len(message.command) == 1:
        await message.reply(
            "📞__ Kindly send the Channel ID or Channel User from where to copy messages along with the command\n\n"
            "Add the bot to the channel and send /id to get the channel ID.\n"
            "\n**Eg:** `/add_forward_channel labelname -10012345678 -> -10087654321` or `/add_forward_channel labelname AmznUser -> -10087654321`\n\n"
            "\nThis Commad Send The New Messages From Other_Person_Channel -> Your_Own_Channel\n"
            "\nNote : Your_Own_Channel Could Be A Group_ID (SuperGroup),Channel_ID , Bot (Username)",
            quote=True
        )
    else:
        if string_session := db.get_string_session(message.from_user.id):
            client = Client(str(int(time.time())), session_string=string_session, api_id=config.API_ID, api_hash=config.API_HASH)
            await client.start()

            label = message.command[1]            
            forwardchannels = message.command[2].split(",")            
            autopostchannels = message.command[4].split(",")
            print(label)
            print(forwardchannels)
            print(autopostchannels)
            
            fchannellist = []
            autochannellist = []

            for fchannel in forwardchannels:
                try:
                    chat_id = int(fchannel)
                except Exception as e:
                    print(e)
                    chat_id = fchannel

                try:
                    channel = await client.join_chat(chat_id)
                except UserAlreadyParticipant:
                    channel = await client.get_chat(chat_id)
                except Exception as e:
                    print(e)
                    return await message.reply("Can't get the Chat, make sure the channel username or channel ID is correct.", quote=True)

                
                fchannellist.append({"id": channel.id, "title": channel.title, "type": channel.type.name})
            
            for autochannel in autopostchannels:
                try:
                    autochannel = int(autochannel)
                except Exception as e:
                    pass
                print("Channel Id-->",channel.id)
                print("Channel Type-->",channel.type)
                a = 10
                if a == 10:
                    print("Inside User Part")
                    try:
                        channel = await bot.get_chat(autochannel)
                    except:
                        try:
                            channel = await client.get_chat(autochannel)
                        except:
                            return await message.reply(f"Kindly add the User to the channel ({autochannel}) with Admin Rights, before sending it to me.", quote=True)
                        return await message.reply(f"Kindly add the bot to the channel ({autochannel}) with Admin Rights, before sending it to me.", quote=True)

                # if channel.type != enums.ChatType.CHANNEL:
                #     return await message.reply("The Chat ID should of a channel only.\n\nAdd the bot to the channel and send /id to get the channel ID.", quote=True)

                if channel.type == enums.ChatType.BOT:
                    print("Inside Bot Part")
                    print(type(autochannel))
                    try:
                        z = await client.resolve_peer(peer_id =autochannel)
                        print(z)
                    except Exception as e:
                        print("peer resolve--->",e)
                    
                    try:                        
                        channel = await client.get_chat(autochannel)
                    except Exception as e:
                        print(e)
                        return await message.reply(f"Kindly start the bot ({autochannel}).", quote=True)

                autochannellist.append({"id": channel.id, "title": channel.title, "type": channel.type.name})

            await client.stop()

            db.add_copy_channel(message.from_user.id, {"label": label, "source": fchannellist, "destination": autochannellist})

            await message.reply(f"Successfully added `{channel.title} ({channel.id})` to the Database for Amazon Links Copying.", quote=True)
        else:
            await message.reply(
                "📞__ Kindly login with your Phone number in the bot in order to copy messages from a Channel.\n\n"
                "**⚠️ Note:**\nDon't forgot to include your Country code.__\n**Eg:** `/connect +13124562345`\n\n",
                quote=True
            )

@Bot.on_message(filters.command("remove_forward_channel") & filters.private)
async def removeCopyChannelFromDB(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the Channel ID along with the command\n\n"
            "\n**Eg:** `/remove_forward_channel -10012345678`\n\n"
            "For get id send /id to get the channel ID in channel which you want to remove.\n"
            "Use /list_forward_channel And Use Souce Id To Remove ",
            quote=True
        )
    else:
        channelIds = message.command[1:]
        print(channelIds)
        for channel in channelIds:
            savedchannel = db.get_all_copy_channel(message.from_user.id)
            print(savedchannel)
            for i in savedchannel :
                source = i['source']
                source = source[0]
                title = source['title']
                source = source['id']
                print(source)
                if str(source) == channel :
                    print("Pass")
                    db.remove_copy_channel(message.from_user.id, i)
                    return await message.reply(f"Successfully Removed `{title} ({channel})` from the Database for Amazon Links Forwarding.", quote=True)

            return await message.reply(f"No such channel id `({channel})` in the Database for Amazon Links Forwarding.", quote=True)

@Bot.on_message(filters.command("reset") & filters.private)
async def reset(bot: Client, message: Message):
    ok = db.reset_all(message.from_user.id)
    if ok ==True:
        return await message.reply("You All The Settings Is Reseted In Database")
    else:
        return await message.reply("No Database Found From Your Id")
    

@Bot.on_message(filters.command("add_footer_channel") & filters.private)
async def addFooterChannel(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.reply(
            "🪪__ Kindly send the Channel Username along with the command\n\n"
            "\n**Eg:** `/add_footer_channel AmznUsers`",
            quote=True
        )
    else:
        channel = message.command[1]
        db.add_custom_footer_channel(message.from_user.id, channel)
        return await message.reply(f"Successfully added @{channel} in the Database for Footer Text Channel.", quote=True)

@Bot.on_message(filters.command("remove_footer_channel") & filters.private)
async def removeFooterChannel(bot: Client, message: Message):
    channel = db.get_custom_footer_channel(message.from_user.id)
    db.remove_custom_footer_channel(message.from_user.id)
    return await message.reply(f"Successfully removed @{channel} from the Database for Footer Text Channel.", quote=True)

@Bot.on_message(filters.command("connect") & filters.private)
async def userLogin(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.reply(
            """Utilize this to forge a connection between your account and the @Amzn_Affiliate_bot. A connection with at least one account is essential to utilize various commands.

Enter the phone number associated with the Telegram account participating in the desired conversations, inclusive of the country code.

Command Parameters
/connect PHONE_NUMBER

Example:
/connect +84444444444


🔊 Stay informed with the latest updates by subscribing to our channel: @AmznUsers""",
            quote=True
        )
    else:
        phone_number = message.command[1]

        client = Client(str(int(time.time())), api_id=config.API_ID, api_hash=config.API_HASH)
        
        client.add_handler(
            MessageHandler(
                lambda c, m: asyncio.create_task(new_message(c, m, message.from_user.id)), filters.channel
            )
        )

        try:
            await client.connect()
            print("clint connected")
        except ConnectionError:
            await client.disconnect()
            await client.connect()

        try:
            code = await client.send_code(phone_number)
            await asyncio.sleep(1)
        except FloodWait as e:
            return await message.reply(f"__Sorry to say you that you have floodwait of {e.value} Seconds 😞__", quote=True)
        except ApiIdInvalid:
            return await message.reply("🕵‍♂ The API ID or API HASH is Invalid.\n\nPress /connect to create again.", quote=True)
        except PhoneNumberInvalid:
            return await message.reply("☎ Your Phone Number is Invalid.`\n\nPress /connect to create again.", quote=True)

        try:
            sent_type = {
                "APP": "Telegram App 💌",
                "SMS": "SMS 💬",
                "CALL": "Phone call 📱",
                "FLASH_CALL": "Phone flash call 📲",
                "EMAIL_CODE": "Email 📧",
                "FRAGMENT_SMS": "Fragment SMS 💬",
                "MISSED_CALL": "Missed call 📱"
            }[code.type.name]

            otp = await message.chat.ask(
                text=(
                    f"I had sent an OTP to the number `{phone_number}` through **{sent_type}**\n\n"
                    "Please enter the OTP in the format `1 2 3 4 5` __(provied white space between numbers)__\n\n"
                    "If Bot not sending OTP then try /connect to the Bot.\n"
                    "Press /cancel to Cancel."
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                listener_type=ListenerTypes.MESSAGE,
                timeout=300
            )
        except TimeoutError:
            return await message.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /connect to create again.", quote=True)

        if await is_cancel(message, otp.text):
            return

        await otp.delete()
        await otp.request.delete()

        otp_code = otp.text
        try:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
        except PhoneCodeInvalid:
            return await message.reply("**📵 Invalid Code**\n\nPress /connect to create again.")
        except PhoneCodeExpired:
            return await message.reply("**⌚ Code is Expired**\n\nPress /connect to create again.")
        except SessionPasswordNeeded:
            try:
                two_step_code = await message.chat.ask(
                    text="`🔐 This account have two-step verification code.\nPlease enter your second factor authentication code.`\nPress /cancel to Cancel.",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    listener_type=ListenerTypes.MESSAGE,
                    timeout=300
                )
            except TimeoutError:
                return await message.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /connect to create again.")

            if await is_cancel(message, two_step_code.text):
                return

            new_code = two_step_code.text
            await two_step_code.delete()
            await two_step_code.request.delete()

            try:
                await client.check_password(new_code)
            except Exception as e:
                return await message.reply(f"**⚠️ ERROR:** `{str(e)}`")
        except Exception as e:
            return await bot.send_message(message.chat.id, f"**⚠️ ERROR:** `{str(e)}`")

        try:
            session_string = await client.export_session_string()

            db.add_string_session(message.from_user.id, session_string)

            logined_user = await client.get_me()

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    text="Logined User ↗️", url=f"tg://openmessage?user_id={logined_user.id}")]]
            )
            await message.reply(f"**✅ Successfully logined with {logined_user.mention} 🧑**", reply_markup=reply_markup, quote=True)
        except Exception as e:
            return await message.reply(f"**⚠️ ERROR:** `{str(e)}`", quote=True)

@Bot.on_message(filters.command("set_tag") & filters.private)
async def set_tag(bot: Bot, message: Message):
    chat_id = message.from_user.id
    if len(message.command) == 1:
        await message.reply(
            "**Send the Amazon Tag along with the command.**\n\n**Eg:** `/set_tag AmznUsers`",
            quote=True,
        )
    else:
        amazon_tag = message.command[1]
        if db.get_amazon_tag(chat_id) == None:
            db.add_amazon_tag(chat_id, amazon_tag)
            await message.reply(
                f"Successfully saved Amazon Tag...\n"
                f"**Amazon Tag id : **`{amazon_tag}` \n",
                quote=True
            )
        else :
            await message.reply(
                "An account is already linked. Please /unset_tag first and try again..", 
                quote=True
            )

@Bot.on_message(filters.command("unset_tag") & filters.private)
async def unset_tag(bot: Bot, message: Message):
    chat_id = message.from_user.id
    amazon_tag = db.get_amazon_tag(chat_id)
    db.remove_amazon_tag(chat_id, amazon_tag)
    await message.reply(
        f"Successfully Removed Amazon Tag i.e **`{amazon_tag}`**...\n\n"
        f"__Hit... /set_tag to link again...__",
        quote=True
    )

@Bot.on_message(filters.command("report") & filters.private)
async def report(client: Client, message: Message):
    chat_id = message.from_user.id
    if not db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#𝐍𝐞𝐰𝐔𝐬𝐞𝐫\n\n᚛› 𝐈𝐃 - `{message.from_user.id}`\n᚛› 𝐍𝐚𝐦𝐞 - [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
            )
        else:
            logging.info(
                f"#NewUser :- Name : {message.from_user.first_name} ID : {message.from_user.id}")
    await message.reply(
        f"**Here is my maker's Telegram contact** : @AmznUsers\n\n"
        f"• __Report a bug...__\n"
        f"• __Suggest Something...__\n"
        f"• __Share Bot Idea...__\n"
        f"• __Give feedback...__\n",
        quote=True
    )

@Bot.on_message(
    filters.private & ~filters.via_bot & (filters.regex(pattern=".*amazon.*") | filters.regex(
        pattern=".*amzn.*")) & ~filters.regex(pattern=".*affiliate-program.amazon.*") & filters.private
)
async def amazon_links(bot: Client, message: Message):
    chat_id = message.from_user.id

    if not db.is_user_exist(chat_id):
        data = await bot.get_me()
        BOT_USERNAME = data.username
        db.add_user(chat_id)

    chat_id = message.from_user.id

    tagAllowed = db.get_tagauthuser(chat_id) == "authorised"

    if BOT_TYPE_PUBLIC is False:
        amazon = Amazon(amazon_tag=db.get_amazon_tag(chat_id) if tagAllowed else None)
    else:
        amazon = Amazon(amazon_tag=db.get_amazon_tag(chat_id))

    status, msg = amazon.check_cookies()
    if not status:
        await message.reply(
            msg,
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
        )

    if message.media:
        oldMessage = message.caption.markdown
        links = extract_links(message.caption)
    else:
        oldMessage = message.text.markdown
        links = extract_links(message.text)

    error = 0
    success = 0
    duplicate = 0
    successLinks = []
    erroredLinks = []
    _temp = await message.reply(
        f"Found `{len(links)}` links.\n\n**📝 Files copy stats:**\n\n**Successfully:** `{success}/{len(links)}`\n**Errors:** `{error}/{len(links)}`\n**Replication:** `{duplicate}/{len(links)}`",
        quote=True,
    )

    for link in links:
        try:
            if link not in successLinks:
                newURL = amazon.generate_url(link)
                if isinstance(newURL, dict):
                    oldMessage = oldMessage.replace(link, newURL['shortUrl'])
                    success += 1
                    successLinks.append(link)
                else:
                    error += 1
                    erroredLinks.append({"link": link, "error": newURL})
            else:
                duplicate += 1
        except:
            error += 1
            erroredLinks.append(
                {
                    "link": link,
                    "error": "Something unexpected. Might not an valid Amazon URL.",
                }
            )

        await _temp.edit(
            f"Found `{len(links)}` links.\n\n**📝 Files copy stats:**\n\n**Successfully:** `{success}/{len(links)}`\n**Errors:** `{error}/{len(links)}`\n**Replication:** `{duplicate}/{len(links)}`"
        )

    footer_channel = db.get_custom_footer_channel(message.from_user.id) or 'AmznUsers'
    oldMessage += f"\n\nShared by @{footer_channel.lstrip('@')}"

    stats = (
        f"Found `{len(links)}` links.\n\n"
        f"**📝 Files copy stats:**\n\n"
        f"**Successfully:** `{success}/{len(links)}`\n"
        f"**Errors:** `{error}/{len(links)}`\n"
        f"**Replication:** `{duplicate}/{len(links)}`\n\n"
    )

    if error > 0:
        stats += "**🌋 Errored Links:**\n\n"
        for index, errorLink in enumerate(erroredLinks):
            stats += f"**{index+1}.** {errorLink['link']}\nError: `{errorLink['error']}`\n\n"

    try:
        await _temp.edit(stats)
    except MessageNotModified:
        pass

    if message.media:
        await message.copy(
            message.from_user.id, caption=oldMessage, reply_to_message_id=message.id
        )
    else:
        await message.reply(oldMessage, disable_web_page_preview=True, quote=True)

    if BOT_TYPE_PUBLIC is False:
        if db.get_forwardauthuser(chat_id) != "authorised":
            return await message.reply(
                "__You dont have access to use **Amazon Tag Feature** of bot.😢__ \n\n **Contact 👉 @AmznUsers To Get Access..😊**", 
                quote=True
            )

    if error == 0:
        if channelID := db.get_forward_channel(message.from_user.id):
            try:
                channel = await bot.get_chat(channelID["id"])
            except:
                db.remove_forward_channel(message.from_user.id, channelID)
                return await message.reply(f"Can't connect to the Channel `{channelID['title']} ({channelID['id']})` Add channel again.", quote=True)

            if message.media:
                await message.copy(
                    channel.id, caption=oldMessage
                )
            else:
                await bot.send_message(channel.id, oldMessage, disable_web_page_preview=True)
    else:
        return await message.reply(f"**Due to error in links, this message is not get forward in Channel**", quote=True)

@Bot.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    user_id = cb.from_user.id
    if cb.data == "notifon":
        notif = db.get_notif(cb.from_user.id)
        if notif is True:
            db.set_notif(user_id, notif=False)
        else:
            db.set_notif(user_id, notif=True)
        await cb.message.edit(
            f"`Here You Can Set Your Settings:`\n\nSuccessfully setted notifications to **{db.get_notif(user_id)}**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"NOTIFICATION  {'🔔' if ((db.get_notif(user_id)) is True) else '🔕'}",
                            callback_data="notifon",
                        )
                    ],
                    [InlineKeyboardButton("❎", callback_data="closeMeh")],
                ]
            ),
        )
        await cb.answer(
            f"Successfully setted notifications to {db.get_notif(user_id)}"
        )
    else:
        await cb.message.delete(True)

async def new_message(client: Client, m: Message, admin_id: int):
    print("In  Mew Message")
    if BOT_TYPE_PUBLIC is False:
        if db.get_forwardauthuser(admin_id) != "authorised":
            return

    tagAllowed = db.get_tagauthuser(admin_id) == "authorised"

    if BOT_TYPE_PUBLIC is False:
        amazon = Amazon(amazon_tag=db.get_amazon_tag(admin_id) if tagAllowed else None)
    else:
        amazon = Amazon(amazon_tag=db.get_amazon_tag(admin_id))
    print("Me here")
    status, msg = amazon.check_cookies()
    if not status:
        await Bot.send_message(
            admin_id,
            text=msg,
            parse_mode=ParseMode.MARKDOWN
        )
    print("Reached So Far")
    for c in db.get_all_copy_channel(admin_id):
        if m.chat.id in [_['id'] for _ in c['source']]:
            if m.media:
                try:
                    oldMessage = m.caption.markdown
                    links = extract_links(m.caption)
                except AttributeError:
                    oldMessage = m.text.markdown
                    links = extract_links(m.text)
            else:
                oldMessage = m.text.markdown
                links = extract_links(m.text)

            error = 0
            success = 0
            duplicate = 0
            successLinks = []
            erroredLinks = []
            print("OKKKKKKKKKKKKK")
            for link in links:
                try:
                    if link not in successLinks:
                        newURL = amazon.generate_url(link)
                        if isinstance(newURL, dict):
                            # oldMessage = oldMessage.replace(
                            #     link, newURL['shortUrl'])
                            oldMessage = oldMessage.replace(link, newURL['shortUrl'])
                            success += 1
                            successLinks.append(link)
                        else:
                            error += 1
                            erroredLinks.append({"link": link, "error": newURL})
                    else:
                        duplicate += 1
                except:
                    error += 1
                    erroredLinks.append(
                        {
                            "link": link,
                            "error": "Something unexpected. Might not an valid Amazon URL.",
                        }
                    )

            if error == 0:
                footer_channel = db.get_custom_footer_channel(admin_id) or 'AmznUsers'
                oldMessage += f"\n\nShared by @{footer_channel.lstrip('@')}"
                print("oldd")
                print(oldMessage)

                if success > 0:
                    if channels := c['destination']:
                        for channelID in channels:
                            try:
                                channel = await Bot.get_chat(channelID["id"])
                            except:
                                try:
                                    print("checking if i can send through ckient")
                                    channel = await c.get_chat(channelID["id"])
                                except:
                                    print("cant send through c")
                                    db.remove_forward_channel(admin_id, channelID)
                                    return await Bot.send_message(
                                        admin_id,
                                        text=f"Can't connect to the Channel `{channelID['title']} ({channelID['id']})` Add channel again.",
                                    )

                                if channel.type != enums.ChatType.BOT:
                                    db.remove_forward_channel(admin_id, channelID)
                                    return await Bot.send_message(
                                        admin_id,
                                        text=f"Can't connect to the Channel `{channelID['title']} ({channelID['id']})` Add channel again.",
                                    )

                            if channel.type == enums.ChatType.BOT:
                                print(channel)
                                print(channel.id)
                                if m.media:
                                    try:
                                        print("trying to copy in bot chat")
                                        await m.copy(
                                            channel.username,
                                            caption=oldMessage
                                        )
                                    except:
                                        await Bot.send_message(
                                            admin_id,
                                            f"Received a Media Message in the channel, kindly add the **{(await c.get_me()).mention}** in the Forward Channel `{channelID['title']} ({channelID['id']})` to also copy the messages with Media."
                                        )
                                else:
                                    print("in else send c")
                                    await client.send_message(channel.username, oldMessage, disable_web_page_preview=True)
                                    print("send1")
                            else:
                                if m.media:
                                    try:
                                        with client:

                                            await m.copy(
                                                channel.id,
                                                caption=oldMessage
                                            )
                                            print("copy")
                                    except:
                                        await Bot.send_message(
                                            admin_id,
                                            f"Received a Media Message in the channel, kindly add the **{(await c.get_me()).mention}** in the Forward Channel `{channelID['title']} ({channelID['id']})` to also copy the messages with Media."
                                        )
                                else:
                                    print("send bot")
                                    await Bot.send_message(channel.id, oldMessage, disable_web_page_preview=True)

async def start_userbots():
    await Bot.start()
    app = web.AppRunner(await web_server())
    await app.setup()       
    await web.TCPSite(app, "0.0.0.0", 8080).start()
    print(f"@{(await Bot.get_me()).username} is successfully started.")

    
    for user in db.get_all_logined_users():
        string_session = user["session_string"][-1]

        UserBot = Client(
            f"{user['id']}-{int(time.time())}",
            session_string=string_session,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
        )

        UserBot.add_handler(
            MessageHandler(
                lambda c, m: asyncio.create_task(new_message(c, m, user["id"])), filters.channel
            )
        )

        try:
            await UserBot.start()
            print("User Bot Started")
        except Exception as e:
            print("Not Started-->",e)
            db.remove_string_session(user["id"], string_session)
        
            try:
                await Bot.send_message(user["id"], f"Hey fellow,\n\nYour Logined session is expired. Kindly relogin using /connect")
            except:
                pass

    await idle()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_userbots())
