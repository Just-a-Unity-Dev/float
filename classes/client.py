from discord import app_commands
import discord

class Client(discord.Client):
    synced = False
    tree: app_commands.CommandTree = None

    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.tree.sync(guild = discord.Object(id = 1020278844231524372))
            self.synced = True

        await self.change_presence(status=discord.Status.idle, activity=discord.Game("D&D 5e"))
        print(f'Bot is now online. Ping is {round(self.latency * 1000)}ms.')
        