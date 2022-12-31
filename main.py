# the discord bot wrapper

from http.client import HTTPException
from classes.client import Client
from discord import app_commands
from dotenv import load_dotenv
import discord
import d20
import os

VERSION = '1.0dev'

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

client = Client()
tree = client.tree

@tree.command(name="info", description="displays some info", guild = discord.Object(id = 1020278844231524372))
async def info(interaction: discord.Interaction):
    embed = discord.Embed(title="float - a D&D bot",description="float is a D&D bot for rolling dice, getting modifiers and more; also fully [open source](https://github.com/Just-a-Unity-Dev/float)!",color=discord.Color.blue())
    embed.add_field(name="version", value=f"running version v{VERSION}")
    embed.set_footer(text=f"this instance is running float v{VERSION}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="modifier", description="with a score, get the appropriate modifier", guild = discord.Object(id = 1020278844231524372))
async def modifier(interaction: discord.Interaction, score: int):
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

    if len(keys) > score or score < 1:
        return await interaction.response.send_message(f"score **{score}** has to be within the range of 1-30.")

    for key in keys:
        modifier = key
        if type(modifier) != tuple:
            modifier = tuple([key])

        if score in modifier: # <number> in (<number>, <number>)
            await interaction.response.send_message(f"with a score of **{score}**, the modifier is `{mod_list[key]}`.")
            break

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
    except HTTPException:
        return await interaction.response.send_message("you roll the dice and it spills into the astral plane never to be seen again.")

client.run(os.getenv('TOKEN'))
