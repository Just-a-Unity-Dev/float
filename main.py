# the discord bot wrapper


from discord.ext.commands import Greedy, Context # or a subclass of yours
from typing import Literal, Optional
from discord.ext import commands

from dotenv import load_dotenv
import discord
import os

VERSION = '1.0dev'

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=".", intents=intents)

@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"synced {len(synced)} commands {'globally' if spec is None else 'to the current guild'}."
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("D&D 5e"))
    print(f'Bot is now online. Ping is {round(client.latency * 1000)}ms.')
    await client.load_extension("classes.cogs.roll")

@client.command(name="info", description="displays some info", guild = discord.Object(id = 1020278844231524372))
async def info(interaction: discord.Interaction):
    embed = discord.Embed(title="float - a D&D bot",description="float is a D&D bot for rolling dice, getting modifiers and more; also fully [open source](https://github.com/Just-a-Unity-Dev/float)!",color=discord.Color.blue())
    embed.add_field(name="version", value=f"running version v{VERSION}")
    embed.set_footer(text=f"this instance is running float v{VERSION}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@client.command(name="modifier", description="with a score, get the appropriate modifier", guild = discord.Object(id = 1020278844231524372))
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

@client.command(name="ping", description="get's the latency of the bot to the discord API.", guild = discord.Object(id = 1020278844231524372))
async def ping(interaction: discord.Interaction):
    """Gets the latency of the bot."""
    await interaction.response.send_message(f'pong. {round(client.latency * 1000)}ms.')

client.run(os.getenv('TOKEN'))
