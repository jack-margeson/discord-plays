import os
import discord
from discord.ext import commands
import logging

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
    print('==================================')

# Command to


@bot.command()
async def roleset(ctx):
    await ctx.send('Test')

# Actually run the bot
bot.run(discordToken)
