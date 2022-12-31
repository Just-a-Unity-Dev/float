
from discord import app_commands
from discord.ext import commands
import discord

class MetaCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.VERSION = "1.0"

    @app_commands.command(name="info", description="displays some info")
    async def info(self, interaction: discord.Interaction):
        """Displays information about the bot"""
        embed = discord.Embed(title="float - a D&D bot",description="float is a D&D bot for rolling dice, getting modifiers and more; also fully [open source](https://github.com/Just-a-Unity-Dev/float)!",color=discord.Color.blue())
        embed.add_field(name="version", value=f"running version v{self.VERSION}")
        embed.set_footer(text=f"this instance is running float v{self.VERSION}")

        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='Invite me to your server', style=discord.ButtonStyle.link, url="https://discord.com/oauth2/authorize?client_id=945995912159834152&permissions=277025737792&scope=bot%20applications.commands"))

        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
    
    @app_commands.command(name="ping", description="get's the latency of the bot to the discord API.")
    async def ping(self, interaction: discord.Interaction):
        """Gets the latency of the bot."""
        await interaction.response.send_message(f'pong. {round(self.client.latency * 1000)}ms.')

async def setup(client: commands.Bot) -> None:
  await client.add_cog(MetaCog(client))