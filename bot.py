import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from game_setup import setup_factory
from utils import split_teams

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
# @commands.has_permissions()
async def setup(ctx, *game):
    """
    setup command that creates channels
    and category based on pre defined games
    """
    if not game:
        await ctx.send("You must specify a game to setup. Example: !setup LoL")
    else:
        await setup_factory(ctx, game[0])


@bot.command()
async def teams(ctx):
    """
    command that splits users in voice channels between teams
    in current channel category
    """

    await split_teams(ctx)


if __name__ == "__main__":
    bot.run(TOKEN)
