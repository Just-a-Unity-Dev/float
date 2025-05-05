from typing import Literal
from discord import app_commands
from discord.ext import commands
import discord
import random


class OracleCog(
    commands.Cog, name="Oracle",
    description="Ask the almighty oracle. Intended for solo-play."
):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name="oracle",
        description="ask the almighty oracle."
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(likelihood="the likelihood of it being correct")
    async def oracle_command_slash(
        self,
        interaction: discord.Interaction,
        likelihood: Literal[
            "50/50",
            "almost impossible",
            "very unlikely",
            "unlikely",
            "likely",
            "very likely",
            "basically certain"
        ]
    ):
        """Ask the almighty oracle."""
        ranks = {
            "almost impossible": 1,
            "very unlikely": 2,
            "unlikely": 3,
            "50/50": 4,
            "likely": 5,
            "very likely": 6,
            "basically certain": 7,
        }

        add = (ranks[likelihood] * 2 - 8)
        result = random.randint(3, 18) + add
        answer = ""
        if result >= 11:
            answer = "yes"
            if result == 11 or result == 12:
                answer += ", but..."
            if result == 17 or result == 18:
                answer += ", and..."
        else:
            answer = "no"
            if result == 9 or result == 10:
                answer += ", but..."
            if result == 3 or result == 4:
                answer += ", and..."

        await interaction.response.send_message(answer)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(OracleCog(client))
