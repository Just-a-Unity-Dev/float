from discord import app_commands
from discord.ext import commands
import discord


class MetaCog(
    commands.Cog,
    name="Meta",
    description="Meta stuff, including displaying information."
):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.VERSION = "1.2.0"

    @commands.hybrid_command(
            name="info",
            brief="information about the bot.",
            description="displays some potentially useful information."
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    async def info(self, ctx: commands.Context):
        """Displays information about the bot"""
        embed = discord.Embed(
            title="float - a dice bot",
            description="""float is a bot for rolling dice.
            fully [open source](https://github.com/Just-a-Unity-Dev/float)!""",
            color=discord.Color.random()
        )
        embed.add_field(name="version", value=f"running version v{self.VERSION}")
        embed.set_footer(text=f"this instance is running float v{self.VERSION}")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(
            label='Invite me to your server!',
            style=discord.ButtonStyle.link,
            url=f"https://discord.com/oauth2/authorize?client_id={self.client.user.id}"
            ))

        await ctx.reply(embed=embed, ephemeral=True, view=view)

    @commands.hybrid_command(
            name="ping",
            brief="pong.",
            description="get's the latency of the bot to the discord API."
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    async def ping(self, ctx: commands.Context):
        """Gets the latency of the bot."""
        await ctx.reply(f'pong. {round(self.client.latency * 1000)}ms.')


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MetaCog(client))
