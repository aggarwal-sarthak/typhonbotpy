import os
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled

class Leave(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(description='Leaves The Server With Given ID', usage=f"{os.path.basename(__file__)[:-3]} <serverid>")
    @command_enabled()
    async def leave(self, ctx: commands.Context):
        if ctx.author.id not in tether.owner_ids: return
        guild = discord.utils.get(self.client.guilds, id=int(ctx))

        if guild:
            await guild.leave()
            await ctx.reply(f"{tether.constants.success} | Left The Server: `{guild.name}`!")
        else:
            await ctx.reply(f"{tether.constants.failed} | No Server Found With Given ID!")

async def setup(client: commands.Bot):
    await client.add_cog(Leave(client))