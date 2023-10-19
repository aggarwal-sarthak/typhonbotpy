from discord.ext import commands
import os
import discord
from validation import is_command_enabled

class firstmsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns First Message In The Channel By The User', usage=f"{os.path.basename(__file__)[:-3]} firstmsg [user]")
    @commands.check(is_command_enabled)
    @commands.bot_has_permissions(embed_links=True, read_message_history=True)
    async def firstmsg(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        async for message in ctx.channel.history(limit=None, oldest_first=True):
            if message.author == member:
                return await message.reply(f"{self.client.emotes['success']} | Found First Message By `{member.name}`!")
                
        await ctx.reply(f"{self.client.emotes['failed']} | No Message Found By `{member.name}`!")

async def setup(client):
    await client.add_cog(firstmsg(client))