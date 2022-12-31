# the discord bot wrapper


from discord.ext.commands import Greedy, Context # or a subclass of yours
from typing import Literal, Optional
from discord.ext import commands

from dotenv import load_dotenv
import discord
import os


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
        elif spec == "%":
            ctx.bot.tree.clear_commands()
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
    # change presence
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("D&D 5e"))
    
    # load extensions
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")
    
    print(f'Bot is now online. Ping is {round(client.latency * 1000)}ms.')

client.run(os.getenv('TOKEN'))
