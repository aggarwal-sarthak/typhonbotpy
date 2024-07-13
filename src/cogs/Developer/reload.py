from discord.ext import commands
import os
from core.check import is_command_enabled

class reload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Reloads A Given Command', usage=f"{os.path.basename(__file__)[:-3]} <cmd>")
    @commands.check(is_command_enabled)
    async def reload(self, ctx, cog: str):
        if ctx.author.id not in self.client.config["owner"]: return
        await self.client.reload_extension(f'cogs.{cog}')
        await ctx.reply(f"{self.client.emotes['success']} | Command {cog} Reloaded Successfully!")

async def setup(client):
    await client.add_cog(reload(client))