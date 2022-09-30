from discord.ext import commands
from dotenv import load_dotenv
import discord
import d20
import os

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

schemas = {}

class Schema():
    def __init__(self) -> None:
        self.fields = {}

    def set_field(self, title, value=None) -> None:
        self.fields.__setitem__(title, value)
        return self.get_field(title=title)
    
    def get_field(self, title):
        return self.fields.__getitem__(title)
    
    def list_schema(self):
        render_output = []
        render_output.append('```')
        render_output.append(f'Schema:')
        if not self.fields:
            render_output.append('No schema data detected. Have you added a field?')
        else:
            for field in self.fields:
                field_data = render_output[field]
                render_output.append(f'{field}: {str(field_data)}')
        render_output.append('```')

        return render_output


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
        print("No schema detected. Creating new schema.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if "schema" in schema:
        return await ctx.reply("a schema is already loaded. use .reset_schema to reset the schema.")

    schema["schema"] = Schema()

    return await ctx.reply("Created a new schema.")

@bot.command()
async def list_schema(ctx):
    """Lists a schema that documents are using."""
    if not ctx.message.guild.id in schemas:
        print("No schema detected. Creating new schema.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if not "schema" in schema:
        return await ctx.reply("a schema has not been set up. use .create_schema to create a schema.")

    return await ctx.reply('\n'.join(schema["schema"].list_schema()))

bot.run(os.getenv('TOKEN'))