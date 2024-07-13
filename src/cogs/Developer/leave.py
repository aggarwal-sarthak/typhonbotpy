from discord.ext import commands
import os
import discord
from core.check import is_command_enabled

class leave(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description='Leaves The Server With Given ID', usage=f"{os.path.basename(__file__)[:-3]} <serverid>")
    @commands.check(is_command_enabled)
    async def leave(self, ctx):
        if ctx.author.id not in self.client.config["owner"]: return
        guild = discord.utils.get(self.client.guilds, id=int(ctx))

        if guild:
            await guild.leave()
            await ctx.reply(f"{self.client.emotes['success']} | Left The server: `{guild.name}`!")
        else:
            await ctx.reply(f"{self.client.emotes['faield']} | No Server Found With Given ID!")

async def setup(client):
    await client.add_cog(leave(client))