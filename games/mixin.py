from typing import List

from discord.utils import get


class Game:
    """mixin for discord game categories"""

    def __init__(self, category: str, teams: List[str]) -> None:
        self._category = category
        self._bot_commands = "bot-commands"
        self._lobby = "Lobby"
        self._teams = teams

    @classmethod
    def _get_category(cls, ctx):
        return get(ctx.guild.categories, name=cls._category) or None

    async def create_category(self):
        """
        creates a category with name param if category
        does not already exist.
        """
        if not self._get_category(self.ctx):
            await self.ctx.guild.create_category(self._category)

    async def create_channels(self):
        """
        creates all channels in the game category if
        channels do not already exist.
        """

        category = self._get_category(self.ctx)

        if not get(
            self.ctx.guild.text_channels,
            name=self._bot_commands,
            category=category,
        ):
            await self.ctx.guild.create_text_channel(
                self._bot_commands, category=category
            )

        if not get(
            self.ctx.guild.voice_channels, name=self._lobby, category=category
        ):
            await self.ctx.guild.create_voice_channel(
                self._lobby, category=category
            )

        for team in self._teams:
            if not get(
                self.ctx.guild.voice_channels, name=team, category=category
            ):
                await self.ctx.guild.create_voice_channel(
                    team, category=category, user_limit=5
                )
