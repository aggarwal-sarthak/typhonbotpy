from discord.ext import commands
import os
from src.core.validation import is_command_enabled

class load(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Loads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    @commands.check(is_command_enabled)
    async def load(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.load_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Loaded Successfully!")

async def setup(client):
    await client.add_cog(load(client))