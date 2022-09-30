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

class DuplicateFieldException(Exception): pass
class ForbiddenFieldException(Exception): pass

class Schema():
    def __init__(self) -> None:
        self.fields = {}
        self.documents = []

    def add_document(self):
        document_fields = {}
        if len(self.documents) == 0:
            document_fields.__setitem__('id', 0)
        else:
            document_fields.__setitem__('id', self.documents[-1].__getitem__('id'))
        
        for field in self.fields:
            document_fields.__setitem__(field, self.fields[field])
        
        self.documents.append(document_fields)
    
    def add_field(self, title, value=None) -> None:
        if title.lower() == 'id':
            raise ForbiddenFieldException
        
        self.set_field(title, value)

        for doc in self.documents:
            doc.__setitem__(title, value)
            print(f'Set {title} to {value}')
        print('Done')

    def set_field(self, title, value=None) -> None:
        if title.lower() == 'id':
            raise ForbiddenFieldException
        self.fields.__setitem__(title.lower(), value)
        return self.get_field(title=title)
    
    def get_field(self, title):
        return self.fields.__getitem__(title.lower())
    
    def list_schema(self):
        render_output = []
        render_output.append('```')
        render_output.append(f'Schema Fields:')
        if not self.fields:
            render_output.append('No field data detected.')
        else:
            for field in self.fields:
                field_data = self.fields[field]
                render_output.append(f'{field}: {str(field_data)}')
        render_output.append('')

        render_output.append('Schema Documents:')
        if not self.documents:
            render_output.append('No documents detected.')
        else:
            for document in self.documents:
                render_output.append('-----')
                for field in document:
                    render_output.append(f'{field}: {document[field]}')
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