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

# Global variable to see if bot is running
isRunning = False


@bot.event
async def on_ready():
    print('Logged in as {0} - {1}'.format(bot.user.name, bot.user.id))
    print('==================================')

# Command to


@bot.command(name='start', brief='Starts reading chat for inputs.',
             help='Stops normal operation and starts reading chat for inputs into the emulator.')
@commands.has_role('Admin')
async def start_command(ctx):
    await ctx.send('Starting to read the chat for inputs...')
    isRunning = True


# Actually run the bot
bot.run(discordToken)
