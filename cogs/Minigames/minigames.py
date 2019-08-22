import asyncio

import discord
from discord.ext import commands

from ..utils.cog import FunCog
from .hangman import Hangman
from .connect4 import Connect4


class Minigames(FunCog):
    """Collection of minigames to play!"""

    def __init__(self, bot):
        super().__init__(bot)
        self._sessions = set()

    def cog_check(self, ctx):
        """Checks if a game is currently running in the channel."""
        return super().cog_check(ctx) and ctx.channel.id not in self._sessions

    async def cog_before_invoke(self, ctx):
        self._sessions.add(ctx.channel.id)

    async def cog_after_invoke(self, ctx):
        self._sessions.remove(ctx.channel.id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            # silence `CheckFailure`s because they spam the console
            pass
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You need another player to play that game.')
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send('Cannot play a game against that member.')
        else:
            raise error

    @commands.command(hidden=True)
    async def blackjack(self, ctx):
        # Proposed by Kootiepatra
        pass

    @commands.command(hidden=True)
    async def boogle(self, ctx):
        # Proposed by Kootiepatra
        pass

    @commands.command(hidden=True)
    async def connect4(self, ctx, other_player: discord.Member):
        """A game of Connect-4 with another member.
        Each player takes turn in placing a token on the board,
        the winner is the first to put four tokens in a row.
        """
        if other_player.bot or other_player == ctx.author:
            raise ValueError('Cannot play a game against that member.')
            
        game = Connect4(ctx, self.bot, other_player)
        await game.play()

    @commands.command()
    async def hangman(self, ctx):
        """A game of Hangman with a random word.
        You guess letters by typing them in chat.
        """
        game = Hangman(ctx, self.bot)
        await game.play()

    @commands.command(hidden=True)
    async def higherlower(self, ctx):
        # Proposed by Outerwebs
        pass

    @commands.command(hidden=True)
    async def mancala(self, ctx):
        # Proposed by Princerbang
        pass

    @commands.command(hidden=True)
    async def tictactoe(self, ctx):
        # Proposed by Princerbang
        pass

    @commands.command(hidden=True)
    async def wordsearch(self, ctx):
        # Proposed by Tant
        pass