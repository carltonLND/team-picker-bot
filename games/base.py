from discord.utils import get


class Game:
    """
    base class containing methods for creating game
    channels

    subclasses must define:
        name: str
        arg: str
        _teams: List
    """

    _bot_commands = "bot-commands"
    _lobby = "Lobby"

    @classmethod
    def _get_category(cls, ctx):
        cls._category = "UTP: " + cls.name
        return get(ctx.guild.categories, name=cls._category) or None

    @classmethod
    async def create_category(cls, ctx):
        """
        creates a category with name param if category
        does not already exist.
        """
        if not cls._get_category(ctx):
            await ctx.guild.create_category(cls._category)

    @classmethod
    async def create_channels(cls, ctx):
        """
        creates all channels in the game category if
        channels do not already exist.
        """

        category = cls._get_category(ctx)

        if not get(
            ctx.guild.text_channels,
            name=cls._bot_commands,
            category=category,
        ):
            await ctx.guild.create_text_channel(
                cls._bot_commands, category=category
            )

        if not get(
            ctx.guild.voice_channels, name=cls._lobby, category=category
        ):
            await ctx.guild.create_voice_channel(cls._lobby, category=category)

        for team in cls._teams:
            if not get(ctx.guild.voice_channels, name=team, category=category):
                await ctx.guild.create_voice_channel(
                    team, category=category, user_limit=5
                )
