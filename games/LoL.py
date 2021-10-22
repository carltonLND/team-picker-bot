from discord.abc import GuildChannel
from discord.utils import get


class LoL(GuildChannel):
    _category = "UTP: League of Legends"
    _bot_commands = "bot-commands"
    _lobby = "Lobby"
    _teams = ["Team 1", "Team 2"]

    def __init__(self, ctx):
        self.ctx = ctx

    @classmethod
    def get_category(cls, ctx):
        return get(ctx.guild.categories, name=cls._category) or None

    async def create_category(self):
        """
        creates a category with name param if category
        does not already exist.
        """
        if not self.get_category(self.ctx):
            await self.ctx.guild.create_category(self._category)

    async def create_commands_channel(self):
        """
        creates text channels from list of channel names
        if they do not exist in category
        """

        category = self.get_category(self.ctx)

        if not get(
            self.ctx.guild.text_channels,
            name=self._bot_commands,
            category=category,
        ):
            await self.ctx.guild.create_text_channel(
                self._bot_commands, category=category
            )

    async def create_lobby_channel(self):
        """
        creates voice channels from list of channel names
        if they do not exist in category
        """

        category = self.get_category(self.ctx)

        if not get(
            self.ctx.guild.voice_channels, name=self._lobby, category=category
        ):
            await self.ctx.guild.create_voice_channel(
                self._lobby, category=category
            )

    async def create_team_channels(self):
        """creates team channels appropriate to game class"""

        category = self.get_category(self.ctx)

        for team in self._teams:
            if not get(
                self.ctx.guild.voice_channels, name=team, category=category
            ):
                await self.ctx.guild.create_voice_channel(
                    team, category=category, user_limit=5
                )

    def get_team_channels(self):
        """
        gets valid team voice channels within category

        returns list containing team objects
        """

        category = self.get_category(self.ctx)

        team_1 = get(
            self.ctx.guild.voice_channels,
            name=self._teams[0],
            category=category,
        )
        team_2 = get(
            self.ctx.guild.voice_channels,
            name=self._teams[1],
            category=category,
        )

        return [team_1, team_2]
