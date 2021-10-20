import os
from random import choice

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

from utils import (
    create_category,
    create_text_channels,
    create_voice_channels,
    get_team_channels,
)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f"{guild.name}(id: {guild.id})")


@bot.command()
async def teams(ctx):
    """
    command that splits users in voice channels between teams
    in current channel category
    """
    if ctx.author.voice and ctx.author.voice.channel:
        game_channel = ctx.author.voice.channel
        if (
            game_channel.name != "Lobby"
            or not game_channel.category.name.startswith("UTP:")
        ):
            await ctx.send(
                "You're not connected to a valid 'Lobby' voice channel."
            )
        else:

            team_channels = get_team_channels(ctx, game_channel.category)
            team_size = len(game_channel.members) / 2

            players = game_channel.members
            if len(players) % 2 == 0 and len(players) <= 10:
                for team in team_channels:
                    while len(team.members) < team_size:
                        player = choice(players)
                        await player.move_to(team)
                        players.remove(player)
            else:
                await ctx.send(
                    "You must have an even number of players, and no more than 10"
                )

    else:
        await ctx.send("You must be connected to a voice channel.")


@bot.command()
# @commands.has_permissions()
async def setup(ctx, *game):
    """
    setup command that creates channels
    and category based on pre defined games
    """
    if not game:
        await ctx.send("You must specify a game to setup. Example: !setup LoL")
    else:
        if game[0].upper() == "LOL":

            text_channels = ["bot-commands"]
            voice_channels = ["Lobby", "Team 1", "Team 2"]

            category = await create_category(ctx, "UTP: League of Legends")
            await create_text_channels(ctx, text_channels, category)
            await create_voice_channels(ctx, voice_channels, category)


if __name__ == "__main__":
    bot.run(TOKEN)
