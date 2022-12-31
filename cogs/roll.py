
from http.client import HTTPException
from discord import app_commands
from discord.ext import commands
import discord
import d20

class RollCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    @app_commands.command(name="guide", description="displays a guide on how to use the bot")
    async def guide(self, interaction: discord.Interaction):
        """Displays information about the bot"""
        desc = """**the basics**
let's roll a basic d20
you can do this via `/roll 1d20`
breaking `1d20` down:
- 1 dice
- of d20

this works for 2d20, etc etc

`/roll` also functions as a full calculator, you can `+-/*` and more.

**binary ops full list**
X * Y - multiplication
X / Y - division
X // Y - int division
X % Y - modulo
X + Y - addition
X - Y - subtraction
X == Y - equality
X >= Y - greater/equal
X <= Y - less/equal
X > Y - greater than
X < Y - less than
X != Y - inequality

**complex stuff**

let's get you into the world of **operators**

operators are always followed by a selector, and operate on the items in the set that match the selector.
k - keep - Keeps all matched values.
p - drop - Drops all matched values.
rr - reroll - Rerolls all matched values until none match. (Dice only)
ro - reroll once - Rerolls all matched values once. (Dice only)
ra - reroll and add - Rerolls up to one matched value once, keeping the original roll. (Dice only)
e - explode on - Rolls another die for each matched value. (Dice only)
mi - minimum - Sets the minimum value of each die. (Dice only)
ma - maximum - Sets the maximum value of each die. (Dice only)

now, **selectors**. selectors select stuff. lol.

X - literal - All values in this set that are literally this value.
hX - highest X - The highest X values in the set.
lX - lowest X - The lowest X values in the set.
>X - greater than X - All values in this set greater than X.
<X - less than X - All values in this set less than X.

**examples**

with all of that said, let's get some examples

`/roll 4d6kh3` - highest 3 of 4 6-sided dice
`/roll 2d6ro<3` - roll 2d6s, then reroll any 1s or 2s once
`/roll 8d6mi2` - roll 8d6s, with each die having a minimum roll of 2"""
        embed = discord.Embed(title="rolling - a guide",description=desc,color=discord.Color.blue())

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="roll", description="rolls a dice. use /guide for guide.")
    async def roll(self, interaction: discord.Interaction, string: str):
        """Roll a dice."""
        try:
            return await interaction.response.send_message(str(d20.roll(string)))
        except d20.RollSyntaxError:
            return await interaction.response.send_message("a syntactic error occured while rolling your dice.")
        except d20.RollValueError:
            return await interaction.response.send_message("a bad value was passed to the operator.")
        except d20.TooManyRolls:
            return await interaction.response.send_message("you roll the dice and it spills all over the floor, you rolled too much dice.")
        except HTTPException:
            return await interaction.response.send_message("you roll the dice and it spills into the astral plane never to be seen again.")

async def setup(client: commands.Bot) -> None:
  await client.add_cog(RollCog(client))