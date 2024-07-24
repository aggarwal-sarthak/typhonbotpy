import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Evaluate(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Evaluates given code",
        aliases=["eval", "e"],
        usage=f"{os.path.basename(__file__)[:-3]} <code>",
    )
    @command_enabled()
    async def evaluate(self, ctx: commands.Context, *, code: str):
        if ctx.author.id not in tether.owner_ids:
            return
        try:
            result = eval(code)
            await ctx.send(f"{tether.constants.success} | **Result:** {result}")

        except Exception as e:
            await ctx.send(f"{tether.constants.failed} | Error: {e}")


async def setup(client: commands.Bot):
    await client.add_cog(Evaluate(client))
