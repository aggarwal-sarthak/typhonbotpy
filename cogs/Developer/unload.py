from discord.ext import commands
import os
from validation import is_command_enabled

class unload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Unloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    @commands.check(is_command_enabled)
    async def unload(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.unload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Unloaded Successfully!")

async def setup(client):
    await client.add_cog(unload(client))