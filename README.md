# 𝓐𝓶𝓪𝔃𝓸𝓷 𝓐𝓯𝓯𝓲𝓵𝓲𝓪𝓽𝓮 𝓑𝓸𝓽

A simple bot to generate your Amazon Affiliate links.

## Features
 - Get Amazon Shorted Affiliate Urls.
 - Support [mongodb.com](https://mongodb.com) database 📁 for user's record 📹.<p align="center">
 - Logs New User's in any channel.
 - Get total user's count in Database. 

## Required Configs
 - `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
 - `API_ID` - Get it from [telegram.org](https://my.telegram.org/auth)
 - `API_HASH` - Get it from [telegram.org](https://my.telegram.org/auth)
 - `AUTH_USERS` - Authorised user's ID to use [Admin Commands](https://github.com/jordngill/amzn-link-cnvrt#admin-commands) {Split 💔 with a space}.
 - `DB_URL` - MongoDB Database URI get it from [mongodb.com](https://mongodb.com)
	- This for Saving UserIDs and Amazon Tags.

## Optional Configs
 - `LOG_CHANNEL` - Log Channel ID to get new user notifications.
	- This for some getting user info. If any new User added to DB, Bot will send Log to that Logs Channel. You can use same DB Channel ID.
- `DB_NAME` - [mongodb.com](https://mongodb.com) Collection name to be used.

## User's Commands 😉

```
start - Start the bot 🥲
settings - Customise settings
connect - Connect your Telegram Account for automated Messages Copying
add_forward_channel - Add a forward Channel
add_copy_channel - Add automated Message Copy Channel
set_tag - Save your Amazon Tag
```

## Admin Commands 🤫

```
stats - Total User Number in Database
```

## Deploy 🚀

### Easiest Heroku Deploy 🤭

<p align="center">
    <a href="https://heroku.com/deploy?template=https://github.com/jordngill/amzn-link-cnvrt">
    <img src="assets/herokudeploy.svg" alt="herokudeploy-01" border="0" height="90" width="285"></a>
</p>

### Host Locally 🤕

```shell
git clone https://github.com/jordngill/amzn-link-cnvrt
cd amzn-link-cnvrt
pip3 install -r requirements.txt
# EDIT config.py values appropriately
python3 main.py
```

## Support Group:

<div style="display: flex; justify-content: space-between;"><a href="https://t.me/AmznUsers"><img src="https://img.shields.io/badge/Telegram-Updates%20Channel-blue.svg?logo=telegram"></a><a href="https://t.me/AmznUsers"><img src="https://img.shields.io/badge/Telegram-Support%20Group-blue.svg?logo=telegram"></a></div>

## Found a Bug 🐛

```Feel free to create a pull or create a issue now and describe your issue freely.```

## Credits
 - [@AmznUsers](https://github.com/jordngill)

<a href="https://pyrogram.org"><img src="https://i.ibb.co/SVLD5k8/Document-1222546317.png" alt="pyrogram" border="0"></a>
