import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from games import supported_games
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
async def setup(ctx, game_key):
    """
    setup command that creates channels
    and category based on pre defined games
    """

    game_key = game_key.upper()

    if game_key not in supported_games:
        return await ctx.send("Error: Invalid game.")

    game = supported_games[game_key]
    await game.create_category(ctx)
    await game.create_channels(ctx)


@setup.error
async def on_command_error(ctx, error):
    """handles errors for !setup bot command"""
    if isinstance(error, commands.errors.MissingRequiredArgument):
        return await ctx.send('Error: No game argument. Example: "!setup LoL"')


@bot.command()
async def teams(ctx):
    """
    command that splits users in voice channels between teams
    in current channel category
    """

    await split_teams(ctx)


if __name__ == "__main__":
    bot.run(TOKEN)
