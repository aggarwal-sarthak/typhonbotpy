import os
import discord
from discord.ext import commands
from src.core.bot import tether
from src.core.check import command_enabled

class Firstmsg(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(description='Returns First Message In The Channel By The User', usage=f"{os.path.basename(__file__)[:-3]} firstmsg [user]")
    @commands.bot_has_permissions(read_message_history=True)
    @command_enabled()
    async def firstmsg(self, ctx: commands.Context, member: discord.Member=None):
        if not member: member = ctx.author

        async for message in ctx.channel.history(limit=None, oldest_first=True):
            if message.author == member:
                return await message.reply(f"{tether.constants.success} | Found First Message By `{member.name}`!")
                
        await ctx.reply(f"{tether.constants.failed} | No Message Found By `{member.name}`!")

async def setup(client: commands.Bot):
    await client.add_cog(Firstmsg(client))