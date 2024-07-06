import discord
from discord.ext import commands
import os

class invite(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(description='Generates Invite Link of a Guild',aliases=['invites'], usage=f"{os.path.basename(__file__)[:-3]} <guild_id>")    
    async def invite(self,ctx,guild: discord.Guild):
        if ctx.author.id not in self.client.config["owner"]: return
        try:
            invite = await guild.invites()
        except discord.Forbidden:
            await ctx.reply(f"{self.client.emotes['failed']} | Missing Permission to generate Invite!")
            return
        except discord.HTTPException:
            await ctx.reply(f"{self.client.emotes['failed']} | An error occurred while fetching the information!")
            return
        await ctx.send(f"{invite[0]}")



async def setup(client):
    await client.add_cog(invite(client))