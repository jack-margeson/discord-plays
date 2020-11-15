# discord-plays 
A Discord bot using discord.py that scans a channel for control inputs that can be customized and fed into keyboard inputs for any game.

[![Netlify Status](https://api.netlify.com/api/v1/badges/e4f8d556-f669-4059-ab24-97d511ab61a2/deploy-status)](https://app.netlify.com/sites/discord-plays/deploys)

## Installation
Clone the repository onto your machine.

Create a virtual environment with Python 3.8.

Activate the virtual environment and run `pip install -r requirements.txt`.

Setup a Google Firestore, get a private key and change line 29 of `discordBotCog.py` with the path to your Google Firestore private key json file.

Setup a Discord bot application and grab the token and replace line 10 `discordbot.py` with the token of your bot.

Run the bot using `python discordbot.py`.

Invite the bot to a server and use `.help` to find a list of commands.


## Contributors
Drew Smith - Controller Backend/Discord Bot

Landon Holland - Discord Bot

Jack Margeson - Website

Cameron Klotter - Website/Discord Bot
