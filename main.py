# the discord bot wrapper

from discord.ext import commands
from dotenv import load_dotenv
from .classes.schema import Schema
import discord
import d20
import os

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

schemas = {}

@bot.event
async def on_ready():
    print(f'Bot is now online. Ping is {round(bot.latency * 1000)}ms.')

@bot.command()
async def ping(ctx):
    """Gets the latency of the bot."""
    await ctx.send(f'pong. {round(bot.latency * 1000)}ms.')

@bot.command()
async def roll(ctx, *args):
    try:
        return await ctx.reply(str(d20.roll(''.join(args))))
    except d20.RollSyntaxError:
        return await ctx.reply("a syntactic error occured while rolling your dice.")
    except d20.RollValueError:
        return await ctx.reply("a bad value was passed to the operator.")
    except d20.TooManyRolls:
        return await ctx.reply("you roll the dice and it spills all over the floor, you rolled too much dice.")

@bot.command()
async def create_schema(ctx):
    """Create's a schema for documents to use."""
    if not ctx.message.guild.id in schemas:
        print("No server detected. Creating new server.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if "schema" in schema:
        return await ctx.reply("a schema is already loaded. use `.reset_schema` to reset the schema.")

    schema["schema"] = Schema()

    return await ctx.reply("created a new schema.")

@bot.command()
async def reset_schema(ctx):
    """Create's a schema for documents to use."""
    if not ctx.message.guild.id in schemas:
        return await ctx.reply("you don't have a schema.")  
    schema = schemas[ctx.message.guild.id]
    schema.__delitem__("schema")
    return await ctx.reply("reset the old schema.")

@bot.command()
async def list_schema(ctx):
    """Lists a schema that documents are using."""
    if not ctx.message.guild.id in schemas:
        print("No server detected. Creating new server.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if not "schema" in schema:
        return await ctx.reply("a schema has not been set up. use `.create_schema` to create a schema.")

    return await ctx.reply('\n'.join(schema["schema"].list_schema()))

@bot.command()
async def add_document(ctx):
    """Adds a document to the schema."""
    if not ctx.message.guild.id in schemas:
        print("No server detected. Creating new server.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if not "schema" in schema:
        return await ctx.reply("a schema has not been set up. use .`create_schema` to create a schema.")

    schema['schema'].add_document()
    return await ctx.reply('added a new document.')

@bot.command()
async def add_field(ctx, field):
    """Adds a field to the schema."""
    if not ctx.message.guild.id in schemas:
        print("No server detected. Creating new server.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if not "schema" in schema:
        return await ctx.reply("a schema has not been set up. use .`create_schema` to create a schema.")

    schema['schema'].add_field(field, 0)
    return await ctx.reply('added a new field.')

bot.run(os.getenv('TOKEN'))