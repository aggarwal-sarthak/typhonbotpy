from discord.ext import commands
import os
import discord
from core.check import is_command_enabled

class membercount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Returns Membercount', usage=f"{os.path.basename(__file__)[:-3]}", aliases= ['members', 'mc'])
    @commands.check(is_command_enabled)
    async def membercount(self, ctx):
        embed = discord.Embed(title=None,color=self.client.config['color'])
        embed.add_field(name='**Members**', value=ctx.guild.member_count)
        embed.timestamp = ctx.message.created_at
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(membercount(client))