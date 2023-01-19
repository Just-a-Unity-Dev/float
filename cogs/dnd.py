
from discord import app_commands
from discord.ext import commands
import discord

class DNDCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="modifier", description="with a score, get the appropriate modifier")
    async def modifier(self, interaction: discord.Interaction, score: int):
        mod_list = {
            (1): -5,
            (2,3): -4,
            (4,5): -3,
            (6,7): -2,
            (8,9): -1,
            (10,11): 0,
            (12,13): 1,
            (14,15): 2,
            (16,17): 3,
            (18,19): 4,
            (20,21): 5,
            (22,23): 6,
            (24,25): 7,
            (26,27): 8,
            (28,29): 9,
            (30): 10
        }
        keys = mod_list.keys()

        if score == 0:
            return await interaction.response.send_message(f"hahahaha. very funny.")

        if score > 30 or score < 1:
            return await interaction.response.send_message(f"score **{score}** has to be within the range of 1-30.")

        for key in keys:
            modifier = key
            if type(modifier) != tuple:
                modifier = tuple([key])

            if score in modifier: # <number> in (<number>, <number>)
                await interaction.response.send_message(f"with a score of **{score}**, the modifier is `{mod_list[key]}`.")
                break

async def setup(client: commands.Bot) -> None:
  await client.add_cog(DNDCog(client))
