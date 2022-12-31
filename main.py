# the discord bot wrapper

from discord.ext import commands
from dotenv import load_dotenv
import discord
import d20
import os

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("D&D 5e"))
    print(f'Bot is now online. Ping is {round(client.latency * 1000)}ms.')

@client.command()
async def ping(ctx):
    """Gets the latency of the bot."""
    await ctx.send(f'pong. {round(client.latency * 1000)}ms.')

@client.command()
async def roll(ctx, *args):
    try:
        return await ctx.reply(str(d20.roll(''.join(args))))
    except d20.RollSyntaxError:
        return await ctx.reply("a syntactic error occured while rolling your dice.")
    except d20.RollValueError:
        return await ctx.reply("a bad value was passed to the operator.")
    except d20.TooManyRolls:
        return await ctx.reply("you roll the dice and it spills all over the floor, you rolled too much dice.")

client.run(os.getenv('TOKEN'))
