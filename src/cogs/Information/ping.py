import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Returns Bot Ping", usage=f"{os.path.basename(__file__)[:-3]}"
    )
    @command_enabled()
    async def ping(self, ctx: commands.Context):
        latency = self.client.latency
        await ctx.reply(f"{tether.constants.success} | {round(latency * 1000)}ms!")


async def setup(client: commands.Bot):
    await client.add_cog(Ping(client))
