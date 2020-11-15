import discord
from discord.ext import tasks, commands
import controller
from collections import deque
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import json

# Cog that holds the bot


class DiscordPlays(commands.Cog):
    def __init__(self):
        self.main_loop.start()

        # variable to see if bot is running in a channel
        self.activeChannels = []

        # config to hold the controls
        self.config = {}
        self.controlsQueue = deque([])

        # variable to store the active game
        self.activeGame = ''

        # Firestore setup
        self.cred = credentials.Certificate(
            "discord-plays-firebase-adminsdk-regue-e6d351cad8.json")
        firebase_admin.initialize_app(credential=self.cred)
        self.db = firestore.client()

        # variable to store the mode
        self.mode = 'anarchy'

    def cog_unload(self):
        self.main_loop.cancel()

    @tasks.loop(seconds=0.5)
    async def main_loop(self):
        if self.config:
            controller.controls_update(
                self.controlsQueue, self.config["activation time"], self.mode)
        else:
            self.controlsQueue.clear()

    # Command to start reading inputs

    @commands.command(name='start', brief='Starts reading chat for inputs.',
                      help='Start normal operation and starts reading chat for inputs into the emulator.\nGameName must be inside of quotes.')
    @commands.has_role('Admin')
    async def start_command(self, ctx, GameName):
        if not ctx.message.channel in self.activeChannels:
            if not self.activeGame:
                print('attempting to load game', GameName)
                try:
                    config = controller.load_config(
                        'games/{0}.json'.format(GameName))
                except FileNotFoundError:
                    print('Error loading game', GameName)
                    raise commands.BadArgument(
                        'Error loading game `{0}`'.format(GameName))
                print('loaded game', GameName)
                self.config = config
                self.activeGame = GameName
                await ctx.bot.change_presence(status=discord.Status.online,
                                              activity=discord.Game(name=self.activeGame))
            embed = self.makeEmbed('Controller', 0x77dd77, 'Activated', 'Now listening to chat in `{0}` for the game `{1}`.'.format(
                ctx.message.channel.name, self.activeGame))
            await ctx.send(embed=embed)
            self.activeChannels.append(ctx.message.channel)
        else:
            embed = self.makeEmbed(
                'Controller', 0xff4055, 'Error', 'Controller is already active.')
            await ctx.send(embed=embed)

    # Command to stop the reading of inputs

    @commands.command(name='stop', brief='Stops reading chat for inputs.',
                      help='Stops normal operation and stops reading chat for inputs into the emulator.')
    @commands.has_role('Admin')
    async def stop_command(self, ctx):
        if ctx.message.channel in self.activeChannels:
            embed = self.makeEmbed(
                'Controller', 0xff4055, 'Deactivated', 'Stopped listening to chat.')
            await ctx.send(embed=embed)
            self.activeChannels.remove(ctx.message.channel)
            if not self.activeChannels:
                self.activeGame = ''
                self.config = {}
                await ctx.bot.change_presence(status=discord.Status.idle, activity=discord.Activity())
        else:
            embed = self.makeEmbed('Controller', 0xff4055, 'Error',
                                   'Controller is currently inactive.')
            await ctx.send(embed=embed)

    # error handling
    @start_command.error
    async def start_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = self.makeEmbed('Controller', 0xff4055, 'Unknown arguments', 'If no game is running type `{0}start` followed by the game.\nIf a game is running in another channel, simply type `{0}start`'.format(
                ctx.bot. command_prefix))
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = self.makeEmbed(
                'Controller', 0xff4055, 'Bad argument', '{0}'.format(error))
            await ctx.send(embed=embed)

    @commands.command(name='list', brief='Lists the available games to play.',
                      help='List the games that can be activated using the play command.')
    async def list_command(self, ctx):
        with open('games/games.json') as json_file:
            gamelist = json.load(json_file)
        message = 'Available games:\n'
        for game in gamelist:
            message = message + game + '\n'
        embed = self.makeEmbed('Controller', 0x77dd77, 'Game List', message)
        await ctx.send(embed=embed)

    @commands.command(name='commands', brief='Lists the available commands for the loaded game.',
                      help='List the commands a user can use while the controller is activated.')
    async def commands_command(self, ctx):
        if self.config:
            message = 'Available commands:\n'
            for action, button in self.config["controls"].items():
                message = message + action + '\n'
            embed = self.makeEmbed(
                'Controller', 0x77dd77, 'Command List', message)
            await ctx.send(embed=embed)
        else:
            embed = self.makeEmbed(
                'Controller', 0xff4055, 'Error', 'No game loaded.')
            await ctx.send(embed=embed)

    @commands.command(name='mode', brief='Sets or shows the mode of the bot.',
                      help='With no arguments it shows the current mode. Valid modes are democracy or anarchy')
    @commands.has_role('Admin')
    async def modeset_command(self, ctx, mode):
        if mode != 'democracy' and mode != 'anarchy':
            raise commands.BadArgument(
                'Invaild mode: valid mode are democracy or anarchy')
        self.mode = mode
        embed = self.makeEmbed(
            'Controller', 0x77dd77, 'Current Mode:', '{0}'.format(self.mode))
        await ctx.send(embed=embed)

    @modeset_command.error
    async def modeset_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingRole):
            embed = self.makeEmbed(
                'Controller', 0x77dd77, 'Current Mode:', '{0}'.format(self.mode))
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = self.makeEmbed(
                'Controller', 0xff4055, 'Bad argument', '{0}'.format(error))
            await ctx.send(embed=embed)

    @commands.command(name='shutdown', brief='Shuts the bot down.',
                      help='Shuts the bot down. Must be Admin to use.')
    @commands.has_role('Admin')
    async def shutdown_command(self, ctx):
        embed = self.makeEmbed(
            'Controller', 0xff4055, 'Shutting down...', 'Bot is shutting down.')
        await ctx.send(embed=embed)
        await ctx.bot.logout()

    # on_message function for eventual reading of inputs

    @ commands.Cog.listener()
    async def on_message(self, message):
        if message.channel in self.activeChannels:
            if message.content in self.config["controls"]:
                # add command to global array
                controller.add_command(
                    self.config["controls"], self.controlsQueue, message.content)

                # add command to firestore, first getting the most recent id to increment
                maxid = self.db.collection(u'commands').document(
                    u'0').get().to_dict()['maxid']

                # add to firestore
                doc_ref = self.db.collection(
                    u'commands').document(str(maxid + 1))
                doc_ref.set({
                    u'name': message.author.display_name,
                    u'command': message.content
                })

                # update maxid
                self.db.collection(u'commands').document(
                    u'0').set({u'maxid': maxid + 1})

    def makeEmbed(self, title, color, name, value):
        embed = discord.Embed(title=title, color=color)
        embed.add_field(name=name,
                        value=value,
                        inline=False)
        embed.set_author(name='discord-plays',
                         icon_url='https://raw.githubusercontent.com/jack-margeson/discord-plays/master/profile_picture.png')
        return embed


def setup(bot):
    # Add cog to bot
    bot.add_cog(DiscordPlays())
