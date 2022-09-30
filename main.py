from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

# load the env so the TOKEN is fed into the environment vars
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

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
    await ctx.send(f'Pong. {round(bot.latency * 1000)}ms.')

bot.run(os.getenv('TOKEN'))