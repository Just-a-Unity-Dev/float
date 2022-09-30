from discord.ext import commands
from dotenv import load_dotenv
import discord
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
    await ctx.send(f'Pong. {round(bot.latency * 1000)}ms.')

@bot.command()
async def create_schema(ctx):
    """Create's a schema for documents to use."""
    if not ctx.message.guild.id in schemas:
        print("No schema detected. Creating new schema.")
        schemas.__setitem__(ctx.message.guild.id, {})
    
    schema = schemas[ctx.message.guild.id]
    if "schema" in schema:
        return await ctx.reply("You, or a previous Gamemaster already has a schema loaded. Use .reset_schema to reset the schema.")

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
        return await ctx.reply("You, or a previous Gamemaster has not set up a schema. Use .create_schema to create a schema.")

    return await ctx.reply('\n'.join(schema["schema"].list_schema()))

bot.run(os.getenv('TOKEN'))