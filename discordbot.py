import os
import discord
from discord.ext import tasks, commands
import logging
import controller
from collections import deque

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

# dictionary to hold the controls
controlsDict = controller.load_controls_dict('controls.json')
controlsQueue = deque([])


@bot.event
async def on_ready():
    print('Logged in as {0} - {1}'.format(bot.user.name, bot.user.id))
    print('discord-plays bot loaded!')
    print('==================================')

# Command to start reading inputs


@bot.command(name='start', brief='Starts reading chat for inputs.',
             help='Stops normal operation and starts reading chat for inputs into the emulator.')
@commands.has_role('Admin')
async def start_command(ctx):
    global isRunning
    await ctx.send('Starting to read the chat for inputs...')
    embed = discord.Embed(title='discord-plays', color=0x6441a5)
    embed.add_field(name='Controller Acvitaved',
                    value='Now listening to chat.', inline=False)
    await ctx.send(embed=embed)
    isRunning = True

# Command to stop the reading of inputs


@bot.command(name='stop', brief='Stops reading chat for inputs.',
             help='Starts normal operation and stops reading chat for inputs into the emulator.')
@commands.has_role('Admin')
async def stop_command(ctx):
    global isRunning
    await ctx.send('Stopping the controller...')
    isRunning = False
# on_message function for eventual reading of inputs


@bot.event
async def on_message(message):
    global isRunning
    global controlsQueue
    global controlsDict
    if isRunning:
        if message.content in controlsDict:
            # add command to global array
            controller.add_command(
                controlsDict, controlsQueue, message.content)

    # Needed to make all other commands work
    await bot.process_commands(message)

# Cog to do stuff every second


class mainLoop(commands.Cog):
    def __init__(self):
        self.main_loop.start()

    def cog_unload(self):
        self.main_loop.cancel()

    @tasks.loop(seconds=1.0)
    async def main_loop(self):
        global controlsQueue
        controller.controls_update(controlsQueue)


# Add cog to bot
bot.add_cog(mainLoop())

# Actually run the bot
bot.run(discordToken)
