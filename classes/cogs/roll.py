
from http.client import HTTPException
from discord import app_commands
from discord.ext import commands
import discord
import d20

class RollCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        
    @app_commands.command(name="roll", description="rolls a dice. use /guide for guide.")
    async def roll(self, interaction: discord.Interaction, string: str):
        try:
            return await interaction.response.send_message(str(d20.roll(string)))
        except d20.RollSyntaxError:
            return await interaction.response.send_message("a syntactic error occured while rolling your dice.")
        except d20.RollValueError:
            return await interaction.response.send_message("a bad value was passed to the operator.")
        except d20.TooManyRolls:
            return await interaction.response.send_message("you roll the dice and it spills all over the floor, you rolled too much dice.")
        except HTTPException:
            return await interaction.response.send_message("you roll the dice and it spills into the astral plane never to be seen again.")

async def setup(client: commands.Bot) -> None:
  await client.add_cog(RollCog(client))