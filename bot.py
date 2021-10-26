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
async def games(ctx):
    """
    command that returns a message listing all
    supported game channels available and their
    setup arguments
    """
    message = ""
    for game in supported_games.values():
        message += f"{game.name}: {game.arg}\r"

    await ctx.send(f"Supported Games:```{message}```")


@bot.command()
async def setup(ctx, game_key):
    """
    setup command that creates channels
    and category based on pre defined games
    """
    game_key = game_key.upper()

    if game_key not in supported_games:
        return await ctx.send("Error: Game not supported. Try: !games")

    game = supported_games[game_key]
    await game.create_category(ctx)
    await game.create_channels(ctx)


@setup.error
async def on_command_error(ctx, error):
    """handles errors for !setup bot command"""
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send('Error: Missing argument. Example: "!setup LoL"')


@bot.command()
async def teams(ctx):
    """
    command that splits users in voice channels between teams
    in current channel category
    """
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("You must be connected to a voice channel.")

    await split_teams(ctx)


if __name__ == "__main__":
    bot.run(TOKEN)
