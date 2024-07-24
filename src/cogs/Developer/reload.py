import os
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled


class Reload(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(
        description="Reloads A Given Command",
        usage=f"{os.path.basename(__file__)[:-3]} <cmd>",
    )
    @command_enabled()
    async def reload(self, ctx: commands.Context, cog: str):
        if ctx.author.id not in tether.owner_ids:
            return
        await self.client.reload_extension(f"src.cogs.{cog}")
        await ctx.reply(
            f"{tether.constants.success} | Command {cog} Reloaded Successfully!"
        )


async def setup(client: commands.Bot):
    await client.add_cog(Reload(client))
