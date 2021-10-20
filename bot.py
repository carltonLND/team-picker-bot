import os
from random import choice

import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

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
    if ctx.author.voice and ctx.author.voice.channel:
        game_channel = ctx.author.voice.channel

        team_1 = get(ctx.guild.voice_channels, name="Team 1")
        team_2 = get(ctx.guild.voice_channels, name="Team 2")

        team_channels = [team_1, team_2]

        players = game_channel.members
        for player in players:
            while player in game_channel.members:
                new_team = choice(team_channels)
                if len(new_team.members) <= len(players) / 2:
                    await player.move_to(new_team)

    else:
        await ctx.send("You're not connected to a voice channel.")


@bot.command()
# @commands.has_permissions()
async def setup(ctx, *game):
    if not game:
        await ctx.send("You must specify a game to setup. Example: !setup LoL")
    else:
        if game[0].upper() == "LOL":

            if not get(ctx.guild.categories, name="UTP: League of Legends"):
                await ctx.guild.create_category("UTP: League of Legends")

            category = get(ctx.guild.categories, name="UTP: League of Legends")

            text_channels = ["bot-commands"]
            for channel in text_channels:
                if not get(
                    ctx.guild.text_channels, name=channel, category=category
                ):
                    await ctx.guild.create_text_channel(
                        channel, category=category
                    )

            voice_channels = ["Lobby", "Team 1", "Team 2"]
            for channel in voice_channels:
                if not get(
                    ctx.guild.voice_channels, name=channel, category=category
                ):
                    await ctx.guild.create_voice_channel(
                        channel, category=category
                    )


if __name__ == "__main__":
    bot.run(TOKEN)
