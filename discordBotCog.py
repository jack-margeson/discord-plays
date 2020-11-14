import discord
from discord.ext import tasks, commands
import controller
from collections import deque


# Cog that hold the bot


class DiscordPlays(commands.Cog):
    def __init__(self):
        self.main_loop.start()

        # variable to see if bot is running in a channel
        self.activeChannels = []

        # dictionary to hold the controls
        self.controlsDict = controller.load_controls_dict('controls.json')
        self.controlsQueue = deque([])

    def cog_unload(self):
        self.main_loop.cancel()

    @tasks.loop(seconds=1.0)
    async def main_loop(self):
        controller.controls_update(self.controlsQueue)

    # Command to start reading inputs

    @commands.command(name='start', brief='Starts reading chat for inputs.',
                      help='Start normal operation and starts reading chat for inputs into the emulator.')
    @commands.has_role('Admin')
    async def start_command(self, ctx):
        if not ctx.message.channel in self.activeChannels:
            embed = discord.Embed(title='Controller', color=0x77dd77)
            embed.add_field(name='Activated',
                            value='Now listening to chat in `{0}`.'.format(ctx.message.channel.name), inline=False)
            embed.set_author(name='discord-plays',
                             icon_url='https://raw.githubusercontent.com/jack-margeson/discord-plays/master/profile_picture.png')
            await ctx.send(embed=embed)
            self.activeChannels.append(ctx.message.channel)
        else:
            embed = discord.Embed(title='Controller', color=0xff4055)
            embed.add_field(
                name='Error', value='Controller is already active.')
            embed.set_author(name='discord-plays',
                             icon_url='https://raw.githubusercontent.com/jack-margeson/discord-plays/master/profile_picture.png')
            await ctx.send(embed=embed)

    # Command to stop the reading of inputs

    @commands.command(name='stop', brief='Stops reading chat for inputs.',
                      help='Stops normal operation and stops reading chat for inputs into the emulator.')
    @commands.has_role('Admin')
    async def stop_command(self, ctx):
        if ctx.message.channel in self.activeChannels:
            embed = discord.Embed(title='Controller', color=0xff4055)
            embed.add_field(name='Deactivated',
                            value='Stopped listening to chat.', inline=False)
            embed.set_author(name='discord-plays',
                             icon_url='https://raw.githubusercontent.com/jack-margeson/discord-plays/master/profile_picture.png')
            await ctx.send(embed=embed)
            self.activeChannels.remove(ctx.message.channel)
        else:
            embed = discord.Embed(title='Controller', color=0xff4055)
            embed.add_field(
                name='Error', value='Controller is currently inactive.')
            embed.set_author(name='discord-plays',
                             icon_url='https://raw.githubusercontent.com/jack-margeson/discord-plays/master/profile_picture.png')
            await ctx.send(embed=embed)

    # on_message function for eventual reading of inputs

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel in self.activeChannels:
            if message.content in self.controlsDict:
                # add command to global array
                controller.add_command(
                    self.controlsDict, self.controlsQueue, message.content)


def setup(bot):
    # Add cog to bot
    bot.add_cog(DiscordPlays())
