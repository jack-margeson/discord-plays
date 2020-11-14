import os
import discord
from discord.ext import tasks, commands
import logging
from discordBotCog import setup

# Code for using dotenv to get Discord token
from dotenv import load_dotenv
load_dotenv()
discordToken = os.getenv("TOKEN")

# Code for setting up logging
logging.basicConfig(level=logging.INFO)

# Intents
intents = discord.Intents.default()

# Initialize bot with command prefix of '.'
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as {0} - {1}'.format(bot.user.name, bot.user.id))
    print('discord-plays bot loaded!')
    print('==================================')

# install cog
setup(bot)

# Actually run the bot
bot.run(discordToken)
