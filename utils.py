from random import choice


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
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("You must be connected to a voice channel.")

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
