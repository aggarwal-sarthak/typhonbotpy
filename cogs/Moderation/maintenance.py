from discord.ext import commands
import os
import discord
from validation import is_command_enabled
    
class maintenance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ | {os.path.basename(__file__)[:-3]} Is Loaded!")

    @commands.group(name='maintenance', description='Enables/Disables Maintenance Mode For Server', usage=f"{os.path.basename(__file__)[:-3]} on/off", aliases=['mm', 'mmode'])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def maintenance(self, ctx):
        pass

    @maintenance.command(name='on', description='Enables Maintenance Mode For Server', usage=f"{os.path.basename(__file__)[:-3]} on", aliases=['enable'])
    @commands.check(is_command_enabled)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def on(self, ctx):
        for channel in ctx.guild.channels:
            if not isinstance(channel, discord.CategoryChannel):
                print(channel)

async def setup(client):
    await client.add_cog(maintenance(client))