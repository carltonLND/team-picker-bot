from discord.abc import GuildChannel

from .mixin import Game


class Lol(GuildChannel, Game):
    _category = "UTP: League of Legends"
    _teams = ["Team 1", "Team 2"]

    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(self._category, self._teams)
