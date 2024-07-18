import discord
from discord.ext import commands
import os
from src.core.bot import tether
from src.core.check import command_enabled

class Invite(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(description='Generates Invite Link of a Guild',aliases=['invites'], usage=f"{os.path.basename(__file__)[:-3]} <guild_id>")
    @command_enabled()
    async def invite(self, ctx: commands.Context , guild: discord.Guild):
        if ctx.author.id not in tether.owner_ids: return
        try:
            invite = await guild.invites()
        except discord.Forbidden:
            await ctx.reply(f"{tether.constants.failed} | Missing Permission To Generate Invite!")
            return
        except discord.HTTPException:
            await ctx.reply(f"{tether.constants.failed} | An Error Occurred While Fetching The Information!")
            return
        await ctx.send(f"{invite[0]}")

async def setup(client: commands.Bot):
    await client.add_cog(Invite(client))