import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from games import supported_games
from utils import CustomHelp, move_to_lobby, split_teams

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences = True

help = CustomHelp(no_category="Bot Commands")
bot = commands.Bot(command_prefix="!", intents=intents, help_command=help)


@bot.event
async def on_ready():
    """
    Prints a list of connected guilds on startup
    """
    print(f"{bot.user} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f"{guild.name}(id: {guild.id})")


@bot.command()
async def lobby(ctx):
    """
    Moves users back to Lobby channel
    """
    channel = ctx.author.voice.channel

    if channel.name == "Lobby" or not channel.category.name.startswith("UTP:"):
        return await ctx.send("Must be connected to a valid team channel.")

    await move_to_lobby(ctx)


@bot.command()
async def games(ctx):
    """
    Lists all currently support games
    """
    message = ""
    for game in supported_games.values():
        message += f"{game.name}: {game.arg}\r"

    await ctx.send(f"Supported Games:```{message}```")


@bot.command()
async def setup(ctx, game_key):
    """
    Create game category Example: !setup LoL
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
    Randomly moves players into team channels
    """
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("You must be connected to a voice channel.")

    await split_teams(ctx)


if __name__ == "__main__":
    bot.run(TOKEN)
