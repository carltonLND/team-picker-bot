from games import supported_games


async def setup_factory(ctx, game_key):
    if game_key.upper() not in supported_games:
        await ctx.send("Game is not yet supported.")

    else:
        game = supported_games[game_key.upper()](ctx)
        await game.create_category()
        await game.create_channels()
