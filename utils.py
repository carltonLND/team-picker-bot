from random import choice

from discord.ext import commands
from discord.utils import get


class CustomHelp(commands.MinimalHelpCommand):
    def get_opening_note(self):
        command_name = self.invoked_with
        return f"Use {self.clean_prefix}{command_name} [command] for more information"


def get_lobby_channel(ctx):
    category = ctx.author.voice.channel.category

    return get(ctx.guild.voice_channels, name="Lobby", category=category)


def get_team_channels(ctx):
    """
    gets valid team voice channels within category

    returns list containing team objects
    """
    category = ctx.author.voice.channel.category

    return [
        channel
        for channel in ctx.guild.voice_channels
        if channel.category == category
    ]


async def move_to_lobby(ctx):

    lobby = get_lobby_channel(ctx)
    team_channels = get_team_channels(ctx)

    for channel in team_channels:
        for player in channel.members:
            await player.move_to(lobby)


async def random_teams(ctx, players):
    """
    assigns players to random team channels within
    their game category as long as they have the right
    amount of players.
    """
    if len(players) % 2 != 0 or len(players) > 10:
        return await ctx.send(
            "You must have an even number of players, and no more than 10"
        )

    team_channels = get_team_channels(ctx)
    team_size = len(players) / 2

    for team in team_channels:
        while len(team.members) < team_size:
            player = choice(players)
            await player.move_to(team)
            players.remove(player)


async def split_teams(ctx):
    """
    splits the teams with a function as long as command
    user is in a valid lobby channel.
    """
    game_channel = ctx.author.voice.channel
    players = game_channel.members

    if (
        game_channel.name != "Lobby"
        or not game_channel.category.name.startswith("UTP:")
    ):
        return await ctx.send(
            "You're not connected to a valid 'Lobby' voice channel."
        )

    await random_teams(ctx, players)
