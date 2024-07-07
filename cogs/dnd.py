from discord.ext import commands
from discord import app_commands


class DNDCog(
    commands.Cog,
    name="D&D 5e",
    description="Utility commands for 5e."
):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.hybrid_command(
            name="modifier",
            aliases=["mod"],
            brief="get ability modifier.",
            description="with a score, get the appropriate modifier."
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    async def modifier(self, ctx: commands.Context, score: int):
        mod_list = {
            (0, 1): -5,
            (2, 3): -4,
            (4, 5): -3,
            (6, 7): -2,
            (8, 9): -1,
            (10, 11): 0,
            (12, 13): 1,
            (14, 15): 2,
            (16, 17): 3,
            (18, 19): 4,
            (20, 21): 5,
            (22, 23): 6,
            (24, 25): 7,
            (26, 27): 8,
            (28, 29): 9,
            (30): 10
        }
        keys = mod_list.keys()

        if score > 30 or score < 0:
            return await ctx.reply(
                f"score **{score}** has to be within the range of 1-30.")

        for key in keys:
            modifier = key
            if modifier is not tuple:
                modifier = tuple([key])

            if score in modifier:  # <number> in (<number>, <number>)
                await ctx.reply(f"**{score}**: mod `{mod_list[key]}`.")
                break


async def setup(client: commands.Bot) -> None:
    await client.add_cog(DNDCog(client))
