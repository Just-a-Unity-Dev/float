# the discord bot wrapper

from discord import app_commands
from dotenv import load_dotenv
import discord
import d20
import os

VERSION = '1.0dev'

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

class Client(discord.Client):
    synced = False

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 1020278844231524372))
            self.synced = True

        await client.change_presence(status=discord.Status.idle, activity=discord.Game("D&D 5e"))
        print(f'Bot is now online. Ping is {round(client.latency * 1000)}ms.')

client = Client()
tree = app_commands.CommandTree(client)

@tree.command(name="ping", description="get's the latency of the bot to the discord API.", guild = discord.Object(id = 1020278844231524372))
async def ping(interaction: discord.Interaction):
    """Gets the latency of the bot."""
    await interaction.response.send_message(f'pong. {round(client.latency * 1000)}ms.')

@tree.command(name="roll", description="rolls a dice. use /guide for guide.", guild = discord.Object(id = 1020278844231524372))
async def roll(interaction: discord.Interaction, string: str):
    try:
        return await interaction.response.send_message(str(d20.roll(string)))
    except d20.RollSyntaxError:
        return await interaction.response.send_message("a syntactic error occured while rolling your dice.")
    except d20.RollValueError:
        return await interaction.response.send_message("a bad value was passed to the operator.")
    except d20.TooManyRolls:
        return await interaction.response.send_message("you roll the dice and it spills all over the floor, you rolled too much dice.")

client.run(os.getenv('TOKEN'))
