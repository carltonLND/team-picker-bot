import os
from random import choice

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

from games.LoL import LoL

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
        if game[0].upper() == "LOL":

            game_LoL = LoL(ctx)

            await game_LoL.create_category()
            await game_LoL.create_commands_channel()
            await game_LoL.create_lobby_channel()
            await game_LoL.create_team_channels()


# @bot.command()
# async def teams(ctx):
#     """
#     command that splits users in voice channels between teams
#     in current channel category
#     """
#     if ctx.author.voice and ctx.author.voice.channel:
#         game_channel = ctx.author.voice.channel
#         if (
#             game_channel.name != "Lobby"
#             or not game_channel.category.name.startswith("UTP:")
#         ):
#             await ctx.send(
#                 "You're not connected to a valid 'Lobby' voice channel."
#             )
#         else:

#             team_channels = self.get_team_channels()
#             team_size = len(game_channel.members) / 2

#             players = game_channel.members
#             if len(players) % 2 == 0 and len(players) <= 10:
#                 for team in team_channels:
#                     while len(team.members) < team_size:
#                         player = choice(players)
#                         await player.move_to(team)
#                         players.remove(player)
#             else:
#                 await ctx.send(
#                     "You must have an even number of players, and no more than 10"
#                 )

#     else:
#         await ctx.send("You must be connected to a voice channel.")


if __name__ == "__main__":
    bot.run(TOKEN)
