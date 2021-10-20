import discord
from discord.ext import commands
from discord.utils import get


async def create_category(ctx, name):
    """
    creates a category with name param if category
    does not already exist.

    returns the category object
    """
    if not get(ctx.guild.categories, name=name):
        await ctx.guild.create_category(name)

    return get(ctx.guild.categories, name=name)


async def create_text_channels(ctx, channels, category):
    """
    creates text channels from list of channel names
    if they do not exist in category
    """
    for channel in channels:
        if not get(
            ctx.guild.text_channels,
            name=channel,
            category=category,
        ):
            await ctx.guild.create_text_channel(channel, category=category)


async def create_voice_channels(ctx, channels, category):
    """
    creates voice channels from list of channel names
    if they do not exist in category
    """
    for channel in channels:
        if not get(ctx.guild.voice_channels, name=channel, category=category):
            if channel == "Lobby":
                await ctx.guild.create_voice_channel(
                    channel, category=category
                )
            else:
                await ctx.guild.create_voice_channel(
                    channel, category=category, user_limit=5
                )


def get_team_channels(ctx, category):
    """
    gets valid team voice channels within category

    returns list containing team objects
    """
    team_1 = get(
        ctx.guild.voice_channels,
        name="Team 1",
        category=category,
    )
    team_2 = get(
        ctx.guild.voice_channels,
        name="Team 2",
        category=category,
    )

    return [team_1, team_2]
